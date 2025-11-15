# core/views_2fa.py
"""
Vues pour la double authentification (2FA)
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from apps.utilisateurs.models import Utilisateur, Code2FA
from apps.utilisateurs.utils_2fa import generer_code_2fa, verifier_code_2fa, verifier_2fa_requis


@login_required(login_url='login')
def activer_2fa(request):
    """Vue pour activer la double authentification"""
    if request.method == 'POST':
        # Générer et envoyer un code de vérification
        try:
            code_2fa = generer_code_2fa(request.user, request)
            messages.success(request, "Un code de vérification a été envoyé à votre adresse email.")
            return redirect('verifier_code_2fa')
        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi du code : {str(e)}")
            return redirect('activer_2fa')
    
    context = {
        'user': request.user,
        'deux_facteurs_actives': request.user.deux_facteurs_actives,
    }
    return render(request, '2fa/activer_2fa.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def verifier_code_2fa_view(request):
    """Vue pour vérifier le code 2FA"""
    if request.method == 'POST':
        code_saisi = request.POST.get('code', '').strip()
        
        if not code_saisi:
            messages.error(request, "Veuillez entrer un code de vérification.")
            return render(request, '2fa/verifier_code_2fa.html')
        
        # Vérifier le code
        if verifier_code_2fa(request.user, code_saisi):
            # Activer le 2FA pour l'utilisateur
            request.user.deux_facteurs_actives = True
            request.user.save()
            
            # Stocker dans la session que le 2FA est vérifié pour cette session
            request.session['2fa_verified'] = True
            request.session['2fa_verified_at'] = timezone.now().isoformat()
            
            messages.success(request, "Double authentification activée avec succès !")
            return redirect('dashboard_enseignant' if request.user.est_enseignant() else 'accueil')
        else:
            messages.error(request, "Code invalide ou expiré. Veuillez réessayer.")
    
    # Vérifier s'il y a un code actif
    code_actif = Code2FA.objects.filter(
        user=request.user,
        utilise=False
    ).order_by('-cree_le').first()
    
    if not code_actif or not code_actif.est_valide():
        messages.warning(request, "Aucun code actif trouvé. Un nouveau code va être envoyé.")
        try:
            generer_code_2fa(request.user, request)
            messages.info(request, "Un nouveau code a été envoyé à votre adresse email.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi du code : {str(e)}")
    
    return render(request, '2fa/verifier_code_2fa.html')


@login_required(login_url='login')
def desactiver_2fa(request):
    """Vue pour désactiver la double authentification"""
    if request.method == 'POST':
        # Vérifier le code 2FA avant de désactiver
        code_saisi = request.POST.get('code', '').strip()
        
        if not code_saisi:
            messages.error(request, "Veuillez entrer votre code de vérification pour désactiver le 2FA.")
            return render(request, '2fa/desactiver_2fa.html')
        
        if verifier_code_2fa(request.user, code_saisi):
            request.user.deux_facteurs_actives = False
            request.user.save()
            
            # Supprimer la vérification de session
            request.session.pop('2fa_verified', None)
            request.session.pop('2fa_verified_at', None)
            
            messages.success(request, "Double authentification désactivée avec succès.")
            return redirect('dashboard_enseignant' if request.user.est_enseignant() else 'accueil')
        else:
            messages.error(request, "Code invalide. Impossible de désactiver le 2FA.")
    
    # Générer un code pour la désactivation
    try:
        generer_code_2fa(request.user, request)
        messages.info(request, "Un code de vérification a été envoyé à votre adresse email.")
    except Exception as e:
        messages.error(request, f"Erreur lors de l'envoi du code : {str(e)}")
    
    return render(request, '2fa/desactiver_2fa.html')


@login_required(login_url='login')
def verifier_2fa_session(request):
    """Vue pour vérifier le code 2FA pour une session (accès à une fonctionnalité protégée)"""
    if request.method == 'POST':
        code_saisi = request.POST.get('code', '').strip()
        next_url = request.POST.get('next', request.GET.get('next', 'accueil'))
        
        if not code_saisi:
            messages.error(request, "Veuillez entrer un code de vérification.")
            return render(request, '2fa/verifier_2fa_session.html', {'next': next_url})
        
        # Vérifier le code
        if verifier_code_2fa(request.user, code_saisi):
            # Stocker dans la session que le 2FA est vérifié
            request.session['2fa_verified'] = True
            request.session['2fa_verified_at'] = timezone.now().isoformat()
            
            messages.success(request, "Code vérifié avec succès.")
            return redirect(next_url)
        else:
            messages.error(request, "Code invalide ou expiré. Veuillez réessayer.")
    
    # Générer un nouveau code si nécessaire
    code_actif = Code2FA.objects.filter(
        user=request.user,
        utilise=False
    ).order_by('-cree_le').first()
    
    if not code_actif or not code_actif.est_valide():
        try:
            generer_code_2fa(request.user, request)
            messages.info(request, "Un code de vérification a été envoyé à votre adresse email.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi du code : {str(e)}")
    
    next_url = request.GET.get('next', 'accueil')
    return render(request, '2fa/verifier_2fa_session.html', {'next': next_url})


def deux_facteurs_required(view_func):
    """
    Décorateur pour forcer la double authentification sur une vue
    """
    from functools import wraps
    
    @login_required(login_url='login')
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Vérifier si le 2FA est requis pour cet utilisateur
        if not verifier_2fa_requis(request.user):
            return view_func(request, *args, **kwargs)
        
        # Vérifier si le 2FA est activé
        if not request.user.deux_facteurs_actives:
            messages.warning(
                request, 
                "Cette fonctionnalité nécessite la double authentification. "
                "Veuillez l'activer dans vos paramètres."
            )
            return redirect('activer_2fa')
        
        # Vérifier si le 2FA a été vérifié dans cette session (valide 30 minutes)
        deux_facteurs_verifie = request.session.get('2fa_verified', False)
        deux_facteurs_verifie_at = request.session.get('2fa_verified_at')
        
        if deux_facteurs_verifie and deux_facteurs_verifie_at:
            try:
                from datetime import datetime
                verified_time = datetime.fromisoformat(deux_facteurs_verifie_at)
                # Vérifier si la vérification est encore valide (30 minutes)
                if (timezone.now() - verified_time).total_seconds() < 1800:
                    return view_func(request, *args, **kwargs)
            except:
                pass
        
        # Rediriger vers la vérification 2FA
        messages.info(request, "Veuillez vérifier votre identité avec le code de double authentification.")
        return redirect(f"{reverse('verifier_2fa_session')}?next={request.path}")
    
    return wrapper

