# core/views_setup.py
"""
Vues temporaires pour configurer le site déployé sur Render
⚠️ À SUPPRIMER après la configuration initiale pour des raisons de sécurité
"""
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from django.core.management.base import CommandError
import os
import json


def _check_secret_token(request):
    """Vérifie le token secret pour sécuriser l'accès"""
    secret_token = os.environ.get('SETUP_SECRET_TOKEN', 'CHANGEZ_MOI_IMMEDIATEMENT')
    provided_token = request.GET.get('token') or request.POST.get('token')
    return provided_token == secret_token


@csrf_exempt
def setup_migrate(request):
    """
    Applique les migrations
    URL: /setup/migrate/?token=VOTRE_TOKEN
    """
    if not _check_secret_token(request):
        return JsonResponse({'error': 'Token invalide'}, status=403)
    
    try:
        from io import StringIO
        output = StringIO()
        call_command('migrate', '--noinput', stdout=output)
        result = output.getvalue()
        return JsonResponse({
            'success': True,
            'message': 'Migrations appliquées avec succès',
            'output': result
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
def setup_create_superuser(request):
    """
    Crée un superutilisateur
    URL: /setup/create-superuser/?token=VOTRE_TOKEN&username=admin&email=admin@example.com&password=MotDePasse123!
    """
    if not _check_secret_token(request):
        return JsonResponse({'error': 'Token invalide'}, status=403)
    
    username = request.GET.get('username') or request.POST.get('username')
    email = request.GET.get('email') or request.POST.get('email')
    password = request.GET.get('password') or request.POST.get('password')
    
    if not all([username, email, password]):
        return JsonResponse({
            'error': 'Paramètres manquants: username, email, password'
        }, status=400)
    
    try:
        from io import StringIO
        output = StringIO()
        call_command(
            'creer_superuser',
            username=username,
            email=email,
            password=password,
            stdout=output
        )
        result = output.getvalue()
        
        # Corriger le type_utilisateur et niveau_acces du superutilisateur créé
        try:
            from apps.utilisateurs.models import Utilisateur
            user = Utilisateur.objects.get(username=username)
            user.type_utilisateur = 'enseignant'
            user.niveau_acces = 'complet'
            user.save()
        except Exception as e:
            # Ne pas bloquer si la correction échoue
            print(f"⚠️  Impossible de corriger le type utilisateur : {e}")
        
        return JsonResponse({
            'success': True,
            'message': f'Superutilisateur "{username}" créé avec succès (enseignant avec accès complet)',
            'output': result
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
def setup_init_programme(request):
    """
    Initialise le programme DESMFMC
    URL: /setup/init-programme/?token=VOTRE_TOKEN&type=detaille
    """
    if not _check_secret_token(request):
        return JsonResponse({'error': 'Token invalide'}, status=403)
    
    programme_type = request.GET.get('type', 'detaille')  # 'base' ou 'detaille'
    
    try:
        from io import StringIO
        output = StringIO()
        
        if programme_type == 'detaille':
            call_command('init_programme_desmfmc_detaille', stdout=output)
        else:
            call_command('init_programme_desmfmc', stdout=output)
        
        result = output.getvalue()
        return JsonResponse({
            'success': True,
            'message': f'Programme DESMFMC initialisé ({programme_type})',
            'output': result
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
def setup_status(request):
    """
    Affiche le statut de la configuration
    URL: /setup/status/?token=VOTRE_TOKEN
    """
    if not _check_secret_token(request):
        return JsonResponse({'error': 'Token invalide'}, status=403)
    
    try:
        from apps.utilisateurs.models import Utilisateur
        
        users_count = Utilisateur.objects.count()
        superusers_count = Utilisateur.objects.filter(is_superuser=True).count()
        
        # Vérifier les migrations
        from django.core.management import call_command
        from io import StringIO
        output = StringIO()
        call_command('showmigrations', '--list', stdout=output)
        migrations_output = output.getvalue()
        
        return JsonResponse({
            'success': True,
            'status': {
                'users_count': users_count,
                'superusers_count': superusers_count,
                'database_connected': True,
                'migrations': migrations_output.split('\n')[:20]  # Premières 20 lignes
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
def setup_dashboard(request):
    """
    Page de dashboard pour la configuration
    URL: /setup/?token=VOTRE_TOKEN
    """
    try:
        if not _check_secret_token(request):
            return HttpResponse('''
            <html>
            <head><title>Accès refusé</title></head>
            <body>
                <h1>❌ Accès refusé</h1>
                <p>Token invalide ou manquant.</p>
                <p>Utilisez: /setup/?token=VOTRE_TOKEN</p>
            </body>
            </html>
            ''', status=403)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return HttpResponse(f'''
        <html>
        <head><title>Erreur</title></head>
        <body>
            <h1>❌ Erreur lors de la vérification du token</h1>
            <p>Erreur : {str(e)}</p>
            <pre>{error_details}</pre>
        </body>
        </html>
        ''', status=500)
    
    try:
        token = request.GET.get('token', '')
        return HttpResponse(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Configuration Render - FMOS MFMC</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                .button {{ display: inline-block; padding: 10px 20px; margin: 5px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }}
                .button:hover {{ background: #0056b3; }}
                .success {{ color: green; }}
                .error {{ color: red; }}
                .output {{ background: #f5f5f5; padding: 10px; border-radius: 5px; margin: 10px 0; white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            <h1>⚙️ Configuration Render - FMOS MFMC</h1>
            
            <h2>Étapes de configuration</h2>
            
            <h3>1. Appliquer les migrations</h3>
            <a href="/setup/migrate/?token={token}" class="button">Appliquer les migrations</a>
            
            <h3>2. Créer un superutilisateur</h3>
            <form method="GET" action="/setup/create-superuser/" style="margin: 10px 0;">
                <input type="hidden" name="token" value="{token}">
                <p>
                    <label>Username: <input type="text" name="username" value="admin" required></label><br>
                    <label>Email: <input type="email" name="email" value="admin@example.com" required></label><br>
                    <label>Password: <input type="password" name="password" required></label><br>
                    <button type="submit" class="button">Créer le superutilisateur</button>
                </p>
            </form>
            
            <h3>3. Initialiser le programme DESMFMC</h3>
            <a href="/setup/init-programme/?token={token}&type=detaille" class="button">Initialiser (détaillé)</a>
            <a href="/setup/init-programme/?token={token}&type=base" class="button">Initialiser (base)</a>
            
            <h3>4. Vérifier le statut</h3>
            <a href="/setup/status/?token={token}" class="button">Vérifier le statut</a>
            
            <hr>
            <p><small>⚠️ Supprimez ces vues après la configuration pour des raisons de sécurité.</small></p>
        </body>
        </html>
        ''')
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return HttpResponse(f'''
        <html>
        <head><title>Erreur</title></head>
        <body>
            <h1>❌ Erreur lors du chargement de la page</h1>
            <p>Erreur : {str(e)}</p>
            <pre>{error_details}</pre>
        </body>
        </html>
        ''', status=500)

