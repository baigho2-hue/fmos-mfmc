# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import models
from django.db.models import Q
from functools import wraps
import json

# Importer les vues du programme DESMFMC
from .views_programme_desmfmc import (
    programme_desmfmc_complet,
    detail_jalon,
    ma_progression_programme,
)

# Importer le modèle pour les coûts des formations
from apps.utilisateurs.models_cout import CoutFormation
# Importer les utilitaires de conversion de devises
from apps.utilisateurs.utils_devise import convertir_montant, formater_montant
# Importer les fonctions pour vérifier l'accès Med 6
from core.views_med6 import a_acces_gratuit_med6

# === Fonctions utilitaires ===
def get_client_ip(request):
    """Récupère l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# === Décorateurs personnalisés ===
def acces_formation_required(view_func):
    """
    Décorateur pour vérifier l'accès aux formations selon le type d'utilisateur.
    - Enseignants avec accès complet : accès à tout
    - Enseignants standard : accès à tout
    - Étudiants : accès selon leur classe
    """
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        user = request.user
        
        # Les enseignants ont toujours accès
        if user.est_enseignant():
            return view_func(request, *args, **kwargs)
        
        # Les étudiants ont accès (on peut ajouter des restrictions par classe plus tard)
        if user.est_etudiant():
            return view_func(request, *args, **kwargs)
        
        # Par défaut, refuser l'accès
        messages.error(request, "Vous n'avez pas accès à cette ressource.")
        return redirect('accueil')
    
    return wrapper

# === Pages principales ===
def index(request):
    return render(request, "accueil.html")

def accueil(request):
    return render(request, 'accueil.html')

def activites(request):
    return render(request, 'activites.html')

def formations(request):
    return render(request, 'formations.html')

def programmes(request):
    return render(request, 'programmes.html')

@login_required(login_url='login')
def cours(request):
    """Page d'accès aux cours pour enseignants et étudiants"""
    return render(request, 'cours.html')

@login_required(login_url='login')
def enseignants(request):
    return render(request, 'enseignants.html')

@login_required(login_url='login')
def etudiants(request):
    return render(request, 'etudiants.html')

@login_required(login_url='login')
def contact(request):
    return render(request, 'contact.html')

def inscription(request):
    from apps.utilisateurs.forms import InscriptionEtudiantForm
    
    if request.method == 'POST':
        # Seuls les étudiants peuvent s'inscrire via cette page
        form = InscriptionEtudiantForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            messages.success(request, "Compte étudiant créé avec succès ! Vous pouvez maintenant vous connecter.")
            return redirect('login')
        else:
            messages.error(request, "Erreur lors de la création du compte. Veuillez vérifier vos informations.")
    else:
        form = InscriptionEtudiantForm()
    
    return render(request, 'inscription.html', {'form': form})

def login_view(request):
    from apps.utilisateurs.forms import LoginForm, CodeVerificationForm
    from apps.utilisateurs.models import Utilisateur
    from apps.utilisateurs.utils import generer_code_verification, verifier_code
    
    # S'assurer que la session est initialisée
    if not hasattr(request, 'session'):
        from django.contrib.sessions.backends.base import SessionBase
        request.session = SessionBase()
    
    # Si l'utilisateur demande de recommencer, supprimer la session
    if request.GET.get('restart') == '1':
        try:
            if 'login_user_id' in request.session:
                del request.session['login_user_id']
            if 'next_url' in request.session:
                del request.session['next_url']
        except (KeyError, AttributeError):
            pass  # Ignorer si la session n'existe pas ou si les clés n'existent pas
        return redirect('login')
    
    # Vérifier si on est à l'étape de vérification du code
    # Utiliser .get() pour éviter KeyError si la clé n'existe pas
    try:
        user_id = request.session.get('login_user_id', None)
    except (KeyError, AttributeError):
        user_id = None
    
    code_form = None
    user = None
    
    if user_id:
        # Étape 2 : Vérification du code
        try:
            user = Utilisateur.objects.get(pk=user_id)
        except Utilisateur.DoesNotExist:
            if 'login_user_id' in request.session:
                del request.session['login_user_id']
            messages.error(request, "Session expirée. Veuillez recommencer.")
            return redirect('login')
        
        # Gérer le renvoi du code
        if request.GET.get('resend') == '1':
            try:
                generer_code_verification(user)
                messages.success(request, f"Un nouveau code de vérification a été envoyé à {user.email}.")
            except Exception as e:
                messages.error(request, f"Erreur lors de l'envoi du code : {str(e)}")
            return redirect('login')
        
        if request.method == 'POST':
            code_form = CodeVerificationForm(request.POST)
            if code_form.is_valid():
                code_saisi = code_form.cleaned_data['code']
                if verifier_code(user, code_saisi):
                    # Code valide, marquer l'email comme vérifié et connecter l'utilisateur
                    if not user.email_verifie:
                        user.email_verifie = True
                        user.save()
                    login(request, user)
                    if 'login_user_id' in request.session:
                        del request.session['login_user_id']
                    messages.success(request, f"Bienvenue {user.get_full_name() or user.username} !")
                    
                    # Redirection selon le paramètre next ou le type d'utilisateur
                    from core.utils_redirect import get_redirect_after_login
                    next_url = request.GET.get('next') or request.session.get('next_url')
                    if next_url:
                        # Nettoyer l'URL next si elle existe dans la session
                        if 'next_url' in request.session:
                            del request.session['next_url']
                        # Vérifier que l'URL est valide
                        if next_url in ['dashboard_etudiant', 'dashboard_enseignant', 'dashboard_administration']:
                            return redirect(next_url)
                    
                    # Redirection intelligente selon le niveau d'accès
                    redirect_url = get_redirect_after_login(user)
                    return redirect(redirect_url)
                else:
                    messages.error(request, "Code de vérification incorrect ou expiré. Veuillez réessayer.")
        else:
            code_form = CodeVerificationForm()
        
        return render(request, 'login.html', {
            'code_form': code_form,
            'user': user,
            'etape_verification': True
        })
    
    # Étape 1 : Authentification username/password
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Stocker l'URL de redirection si présente
            next_url = request.GET.get('next')
            if next_url:
                request.session['next_url'] = next_url
            
            # Les superutilisateurs peuvent se connecter directement sans vérification
            if user.is_superuser:
                login(request, user)
                if not user.email_verifie:
                    user.email_verifie = True
                    user.save()
                messages.success(request, f"Bienvenue {user.get_full_name() or user.username} !")
                
                # Redirection selon le paramètre next ou le type d'utilisateur
                from core.utils_redirect import get_redirect_after_login
                if next_url:
                    # Nettoyer l'URL next si elle existe dans la session
                    if 'next_url' in request.session:
                        del request.session['next_url']
                    # Vérifier que l'URL est valide
                    if next_url in ['dashboard_etudiant', 'dashboard_enseignant', 'dashboard_administration']:
                        return redirect(next_url)
                
                # Redirection intelligente selon le niveau d'accès
                redirect_url = get_redirect_after_login(user)
                return redirect(redirect_url)
            
            # Générer et envoyer le code de vérification pour les autres utilisateurs
            try:
                generer_code_verification(user)
                # Stocker l'ID de l'utilisateur en session pour l'étape suivante
                request.session['login_user_id'] = user.id
                messages.info(request, f"Un code de vérification a été envoyé à {user.email}. Veuillez l'entrer ci-dessous.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Erreur lors de l'envoi du code de vérification : {str(e)}")
        else:
            messages.error(request, "Erreur de connexion. Vérifiez vos identifiants.")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {
        'form': form,
        'etape_verification': False
    })

def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('accueil')

# === Dashboards ===
@login_required(login_url='login')
def dashboard_etudiant(request):
    from apps.utilisateurs.models_formation import Classe, Cours, ProgressionEtudiant, Planification
    from django.utils import timezone
    from datetime import timedelta
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_etudiant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    user = request.user
    classe_obj = user.get_classe_obj()
    
    # Si l'étudiant est Med 6 avec accès gratuit, afficher tous les cours Med 6
    if a_acces_gratuit_med6(user):
        from apps.utilisateurs.models_formation import Classe
        try:
            classe_med6 = Classe.objects.filter(nom__icontains='Médecine 6').first()
            if classe_med6:
                cours_list = Cours.objects.filter(classe=classe_med6, actif=True).order_by('ordre', 'date_debut')
            else:
                cours_list = Cours.objects.none()
        except:
            cours_list = Cours.objects.none()
    # Récupérer les cours de la classe de l'étudiant
    elif classe_obj:
        cours_list = Cours.objects.filter(classe=classe_obj, actif=True).order_by('ordre', 'date_debut')
    else:
        cours_list = Cours.objects.none()  # QuerySet vide au lieu d'une liste
    
    # Récupérer ou initialiser les progressions de l'étudiant pour les cours de sa classe
    progressions = ProgressionEtudiant.objects.filter(etudiant=user).select_related('cours')
    progression_dict = {p.cours_id: p for p in progressions}

    for cours in cours_list:
        if cours.id not in progression_dict:
            progression, _ = ProgressionEtudiant.objects.get_or_create(
                etudiant=user,
                cours=cours,
                defaults={
                    'statut': 'non_commence',
                    'pourcentage_completion': 0,
                }
            )
            progression_dict[cours.id] = progression

    # Actualiser la liste de progressions après éventuelles créations
    progressions = list(progression_dict.values())

    # Préparer les informations de planification par cours (présentation et évaluation)
    cours_infos = []
    if cours_list:
        planifs_associees = Planification.objects.filter(
            cours_lie__in=cours_list,
            actif=True
        ).select_related('cours_lie').order_by('date_debut')

        presentations_par_cours = {}
        evaluations_par_cours = {}

        for planif in planifs_associees:
            if not planif.cours_lie_id:
                continue

            if planif.type_activite in ['cours', 'td', 'tp', 'atelier', 'conference']:
                presentations_par_cours.setdefault(planif.cours_lie_id, planif)
            elif planif.type_activite in ['evaluation', 'examen']:
                evaluations_par_cours.setdefault(planif.cours_lie_id, planif)

        for cours in cours_list:
            cours_infos.append({
                'cours': cours,
                'planif_presentation': presentations_par_cours.get(cours.id),
                'planif_evaluation': evaluations_par_cours.get(cours.id),
            })
    
    # Récupérer la planification de la classe (fenêtre glissante et activités en cours)
    if classe_obj:
        maintenant = timezone.now()
        date_limite = maintenant + timedelta(days=90)
        planifications = Planification.objects.filter(
            classe=classe_obj,
            actif=True,
        ).filter(
            date_debut__lte=date_limite,
            date_fin__gte=maintenant
        ).order_by('date_debut', 'date_fin')
    else:
        planifications = Planification.objects.none()  # QuerySet vide
    
    # Calculer la progression globale
    total_cours = cours_list.count()
    cours_termines = sum(1 for p in progressions if p.statut in ['termine', 'valide'])
    pourcentage_global = (cours_termines / total_cours * 100) if total_cours > 0 else 0
    
    # Récupérer les lettres d'informations destinées à l'étudiant
    from apps.utilisateurs.models_documents import LettreInformation
    try:
        # Filtrer les lettres d'informations pour cet étudiant
        lettres_query = LettreInformation.objects.filter(actif=True)
        
        # Si l'étudiant a une classe, inclure les lettres pour sa classe
        if classe_obj:
            lettres_information = lettres_query.filter(
                Q(destinataires=user) | Q(classe_cible=classe_obj) | Q(classe_cible__isnull=True)
            ).distinct().order_by('-date_envoi')[:5]
        else:
            # Sinon, seulement les lettres où l'étudiant est destinataire ou lettres générales
            lettres_information = lettres_query.filter(
                Q(destinataires=user) | Q(classe_cible__isnull=True)
            ).distinct().order_by('-date_envoi')[:5]
    except Exception as e:
        # En cas d'erreur, logger l'erreur et retourner une liste vide
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erreur lors de la récupération des lettres d'information: {str(e)}", exc_info=True)
        lettres_information = LettreInformation.objects.none()
    
    context = {
        'user': user,
        'classe_obj': classe_obj,
        'cours_list': cours_list,
        'cours_infos': cours_infos,
        'progression_dict': progression_dict,
        'planifications': planifications,
        'total_cours': total_cours,
        'cours_termines': cours_termines,
        'pourcentage_global': round(pourcentage_global, 1),
        'lettres_information': lettres_information,
    }
    
    return render(request, 'dashboard_etudiant.html', context)

@login_required(login_url='login')
def dashboard_enseignant(request):
    from apps.utilisateurs.models_formation import Cours, Classe, ProgressionEtudiant, SessionCoursEnLigne, SessionEvaluationEnLigne
    from apps.evaluations.models import EvaluationEnseignant
    from apps.utilisateurs.models import Utilisateur
    from django.db.models import Count, Avg, Q, F
    from django.utils import timezone
    from collections import defaultdict
    import json
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    user = request.user
    
    # Récupérer les cours de l'enseignant
    cours_list = Cours.objects.filter(
        Q(enseignant=user) | Q(co_enseignants=user),
        actif=True
    ).distinct().order_by('-date_modification')
    
    # Récupérer toutes les classes où l'enseignant enseigne
    classes_enseignees = Classe.objects.filter(
        cours__in=cours_list
    ).distinct()
    
    # Récupérer les noms des classes pour la requête
    noms_classes = list(classes_enseignees.values_list('nom', flat=True))
    
    # Nombre total d'étudiants dans toutes les classes
    # Utiliser une requête qui compare le champ texte 'classe' avec les noms des classes
    total_etudiants = 0
    if noms_classes:
        # Créer une condition Q pour chaque nom de classe (recherche partielle)
        q_objects = Q()
        for nom_classe in noms_classes:
            q_objects |= Q(classe__icontains=nom_classe)
        
        # Combiner avec le filtre type_utilisateur
        q_objects &= Q(type_utilisateur='etudiant')
        
        total_etudiants = Utilisateur.objects.filter(
            q_objects
        ).distinct().count()
    
    # Étudiants avec défis de progression (progression < 50% ou statut non_commence/en_cours depuis longtemps)
    etudiants_defis = []
    for cours in cours_list:
        progressions = ProgressionEtudiant.objects.filter(
            cours=cours
        ).select_related('etudiant')
        
        for progression in progressions:
            # Défis : progression < 50% ou non commencé depuis plus de 2 semaines
            jours_sans_activite = (timezone.now() - progression.derniere_activite).days if progression.derniere_activite else 999
            if progression.pourcentage_completion < 50 or (progression.statut in ['non_commence', 'en_cours'] and jours_sans_activite > 14):
                etudiants_defis.append({
                    'etudiant': progression.etudiant,
                    'cours': cours,
                    'progression': progression,
                    'jours_sans_activite': jours_sans_activite
                })
    
    # Supprimer les doublons (même étudiant dans plusieurs cours)
    etudiants_defis_unique = {}
    for item in etudiants_defis:
        etudiant_id = item['etudiant'].id
        if etudiant_id not in etudiants_defis_unique:
            etudiants_defis_unique[etudiant_id] = item
        else:
            # Garder celui avec la progression la plus faible
            if item['progression'].pourcentage_completion < etudiants_defis_unique[etudiant_id]['progression'].pourcentage_completion:
                etudiants_defis_unique[etudiant_id] = item
    
    etudiants_defis = list(etudiants_defis_unique.values())[:10]  # Limiter à 10
    
    # Matières/cours terminés
    cours_termines = cours_list.filter(
        date_fin__lt=timezone.now().date()
    ).count()
    
    # Évaluations de l'enseignant par les étudiants
    evaluations_enseignant = EvaluationEnseignant.objects.filter(
        enseignant=user
    )
    
    # Statistiques d'évaluation
    stats_evaluation = {
        'total': evaluations_enseignant.count(),
        'moyenne_qualite_pedagogique': evaluations_enseignant.aggregate(Avg('qualite_pedagogique'))['qualite_pedagogique__avg'] or 0,
        'moyenne_disponibilite': evaluations_enseignant.aggregate(Avg('disponibilite'))['disponibilite__avg'] or 0,
        'moyenne_clarte': evaluations_enseignant.aggregate(Avg('clarte_explications'))['clarte_explications__avg'] or 0,
        'moyenne_gestion_classe': evaluations_enseignant.aggregate(Avg('gestion_classe'))['gestion_classe__avg'] or 0,
    }
    
    # Données pour le graphique d'évaluation (format JSON pour le template)
    graphique_evaluation = {
        'labels': json.dumps(['Qualité pédagogique', 'Disponibilité', 'Clarté', 'Gestion de classe']),
        'scores': json.dumps([
            float(round(stats_evaluation['moyenne_qualite_pedagogique'], 1)),
            float(round(stats_evaluation['moyenne_disponibilite'], 1)),
            float(round(stats_evaluation['moyenne_clarte'], 1)),
            float(round(stats_evaluation['moyenne_gestion_classe'], 1)),
        ])
    }
    
    # Méthodes pédagogiques appréciées
    from apps.utilisateurs.models_formation import MethodePedagogique
    methodes_appreciees = {}
    
    # Récupérer les méthodes utilisées dans les cours de l'enseignant
    for cours in cours_list:
        for methode in cours.methodes_pedagogiques.all():
            if methode.id not in methodes_appreciees:
                methodes_appreciees[methode.id] = {
                    'methode': methode,
                    'cours_count': 0,
                    'appreciation': 0  # À calculer depuis les évaluations
                }
            methodes_appreciees[methode.id]['cours_count'] += 1
    
    # Trier par nombre de cours utilisant la méthode
    methodes_appreciees = sorted(
        methodes_appreciees.values(),
        key=lambda x: x['cours_count'],
        reverse=True
    )[:5]
    
    # Sessions de cours en ligne
    sessions_cours = SessionCoursEnLigne.objects.filter(
        enseignant=user
    ).order_by('-date_debut_prevue')[:5]
    
    # Sessions d'évaluation
    sessions_eval = SessionEvaluationEnLigne.objects.filter(
        enseignant=user
    ).order_by('-date_debut_prevue')[:5]
    
    # Récupérer les lettres d'informations (enseignants peuvent voir toutes)
    from apps.utilisateurs.models_documents import LettreInformation
    lettres_information = LettreInformation.objects.filter(
        actif=True
    ).order_by('-date_envoi')[:5]
    
    context = {
        'user': user,
        'cours_list': cours_list[:10],  # Limiter à 10 pour l'affichage
        'total_cours': cours_list.count(),
        'classes_enseignees': classes_enseignees,
        'total_etudiants': total_etudiants,
        'etudiants_defis': etudiants_defis,
        'cours_termines': cours_termines,
        'stats_evaluation': stats_evaluation,
        'graphique_evaluation': graphique_evaluation,
        'methodes_appreciees': methodes_appreciees,
        'sessions_cours': sessions_cours,
        'sessions_eval': sessions_eval,
        'lettres_information': lettres_information,
    }
    
    return render(request, 'dashboard_enseignant.html', context)


# === Vues pour étudiants ===
@login_required(login_url='login')
def mes_cours(request):
    from apps.utilisateurs.models_formation import Classe, Cours, ProgressionEtudiant
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_etudiant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    user = request.user
    classe_obj = user.get_classe_obj()
    
    # Si l'étudiant est Med 6 avec accès gratuit, afficher tous les cours Med 6
    if a_acces_gratuit_med6(user):
        from apps.utilisateurs.models_formation import Classe
        try:
            classe_med6 = Classe.objects.filter(nom__icontains='Médecine 6').first()
            if classe_med6:
                cours_list = Cours.objects.filter(classe=classe_med6, actif=True).order_by('ordre', 'date_debut')
            else:
                cours_list = Cours.objects.none()
        except:
            cours_list = Cours.objects.none()
    elif not classe_obj:
        messages.warning(request, "Aucune classe associée à votre compte. Veuillez contacter l'administration.")
        return redirect('dashboard_etudiant')
    else:
        cours_list = Cours.objects.filter(classe=classe_obj, actif=True).order_by('ordre', 'date_debut')
    progressions = ProgressionEtudiant.objects.filter(etudiant=user).select_related('cours')
    # Créer un dictionnaire avec les IDs des cours comme clés
    progression_dict = {}
    for p in progressions:
        progression_dict[p.cours.id] = p
    
    return render(request, 'etudiant/mes_cours.html', {
        'cours_list': cours_list,
        'progression_dict': progression_dict,
        'classe_obj': classe_obj,
    })


@login_required(login_url='login')
def detail_cours(request, cours_id):
    from apps.utilisateurs.models_formation import Cours, ProgressionEtudiant, Lecon
    from django.shortcuts import get_object_or_404
    
    if not request.user.est_etudiant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    user = request.user
    cours = get_object_or_404(Cours, pk=cours_id, actif=True)
    
    # Vérifier si l'étudiant est Med 6 avec accès gratuit (6ème année uniquement)
    if a_acces_gratuit_med6(user):
        # Les étudiants de 6ème année de médecine ont accès gratuit UNIQUEMENT aux cours de Médecine 6
        # Sauf s'ils se sont inscrits à une autre formation (mais pas DESMFMC sans validation)
        if not cours.classe or 'Médecine 6' not in cours.classe.nom:
            # Vérifier si l'étudiant s'est inscrit à une autre formation
            classe_obj = user.get_classe_obj()
            if classe_obj and cours.classe == classe_obj:
                # L'étudiant s'est inscrit à cette formation, accès autorisé
                pass
            else:
                # Vérifier si c'est une formation DESMFMC (nécessite validation)
                if cours.classe and cours.classe.formation:
                    formation = cours.classe.formation
                    if 'DESMFMC' in formation.nom.upper() or 'DESMFMC' in formation.code.upper():
                        messages.warning(
                            request, 
                            "L'accès au programme DESMFMC nécessite une validation des conditions d'accès. "
                            "Veuillez contacter l'administration pour plus d'informations."
                        )
                        return redirect('mes_cours')
                    else:
                        messages.warning(
                            request, 
                            "Ce cours n'est pas destiné aux étudiants de 6ème année de médecine. "
                            "Vous devez vous inscrire à cette formation pour y accéder."
                        )
                        return redirect('mes_cours')
                else:
                    messages.warning(request, "Ce cours n'est pas destiné aux étudiants de 6ème année de médecine.")
                    return redirect('mes_cours')
    # Vérifier que l'étudiant a accès à ce cours (même classe)
    elif not request.user.is_superuser:
        classe_obj = user.get_classe_obj()
        if not classe_obj or cours.classe != classe_obj:
            messages.error(request, "Vous n'avez pas accès à ce cours.")
            return redirect('mes_cours')
    
    # Récupérer ou créer la progression
    progression, created = ProgressionEtudiant.objects.get_or_create(
        etudiant=user,
        cours=cours,
        defaults={'statut': 'non_commence'}
    )
    
    # Récupérer les leçons du cours, triées par ordre
    lecons = Lecon.objects.filter(cours=cours, actif=True).order_by('ordre', 'numero')
    
    # Récupérer les progressions des leçons pour cet étudiant
    from apps.utilisateurs.models_formation import ProgressionLecon
    progressions_lecons = ProgressionLecon.objects.filter(
        etudiant=user,
        lecon__in=lecons
    ).select_related('lecon')
    progression_lecons_dict = {p.lecon_id: p for p in progressions_lecons}
    
    # Récupérer les quiz et commentaires pour chaque leçon
    from apps.utilisateurs.models_formation import QuizLecon, CommentaireLecon
    lecons_avec_details = []
    for lecon in lecons:
        lecon_data = {
            'lecon': lecon,
            'progression': progression_lecons_dict.get(lecon.id),
            'quiz': QuizLecon.objects.filter(lecon=lecon, actif=True).order_by('ordre'),
            'commentaires': CommentaireLecon.objects.filter(lecon=lecon, actif=True, parent__isnull=True).order_by('-date_creation')[:5],
        }
        lecons_avec_details.append(lecon_data)
    
    return render(request, 'etudiant/detail_cours.html', {
        'cours': cours,
        'progression': progression,
        'lecons_avec_details': lecons_avec_details,
    })


@login_required(login_url='login')
def ma_progression(request):
    from apps.utilisateurs.models_formation import Classe, Cours, ProgressionEtudiant
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_etudiant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    user = request.user
    classe_obj = user.get_classe_obj()
    
    if not classe_obj:
        messages.warning(request, "Aucune classe associée à votre compte.")
        return redirect('dashboard_etudiant')
    
    cours_list = Cours.objects.filter(classe=classe_obj, actif=True).order_by('ordre', 'date_debut')
    progressions = ProgressionEtudiant.objects.filter(etudiant=user, cours__in=cours_list).select_related('cours')
    
    # Statistiques
    total_cours = cours_list.count()
    stats = {
        'non_commence': progressions.filter(statut='non_commence').count(),
        'en_cours': progressions.filter(statut='en_cours').count(),
        'termine': progressions.filter(statut='termine').count(),
        'valide': progressions.filter(statut='valide').count(),
    }
    
    return render(request, 'etudiant/ma_progression.html', {
        'cours_list': cours_list,
        'progressions': progressions,
        'stats': stats,
        'total_cours': total_cours,
        'classe_obj': classe_obj,
    })


@login_required(login_url='login')
def ma_planification(request):
    from apps.utilisateurs.models_formation import Classe, Planification
    from django.utils import timezone
    from datetime import timedelta
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_etudiant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    user = request.user
    classe_obj = user.get_classe_obj()
    
    if not classe_obj:
        messages.warning(request, "Aucune classe associée à votre compte.")
        return redirect('dashboard_etudiant')
    
    # Récupérer les planifications (mois en cours et suivant)
    date_debut = timezone.now()
    date_fin = date_debut + timedelta(days=60)
    
    planifications = Planification.objects.filter(
        classe=classe_obj,
        actif=True,
        date_debut__gte=date_debut,
        date_debut__lte=date_fin
    ).order_by('date_debut')
    
    # Grouper par date
    planifications_par_date = {}
    for planif in planifications:
        date_key = planif.date_debut.date()
        if date_key not in planifications_par_date:
            planifications_par_date[date_key] = []
        planifications_par_date[date_key].append(planif)
    
    return render(request, 'etudiant/ma_planification.html', {
        'planifications': planifications,
        'planifications_par_date': planifications_par_date,
        'classe_obj': classe_obj,
    })


# === Vues pour enseignants ===
@login_required(login_url='login')
def mes_cours_enseignant(request):
    """Liste des cours de l'enseignant"""
    from apps.utilisateurs.models_formation import Cours
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    user = request.user
    cours_list = Cours.objects.filter(
        models.Q(enseignant=user) | models.Q(co_enseignants=user),
        actif=True
    ).distinct().order_by('-date_modification')
    
    return render(request, 'enseignant/mes_cours.html', {
        'cours_list': cours_list,
    })


@login_required(login_url='login')
def modifier_cours(request, cours_id):
    """Modifier un cours (enseignant uniquement)"""
    from apps.utilisateurs.models_formation import Cours
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    cours = get_object_or_404(Cours, pk=cours_id, actif=True)
    
    # Vérifier que l'enseignant est propriétaire ou co-enseignant
    if cours.enseignant != request.user and request.user not in cours.co_enseignants.all():
        messages.error(request, "Vous n'avez pas le droit de modifier ce cours.")
        return redirect('mes_cours_enseignant')
    
    if request.method == 'POST':
        cours.titre = request.POST.get('titre', cours.titre)
        cours.description = request.POST.get('description', cours.description)
        cours.contenu = request.POST.get('contenu', cours.contenu)
        cours.save()
        messages.success(request, "Cours modifié avec succès.")
        return redirect('modifier_cours', cours_id=cours.id)
    
    return render(request, 'enseignant/modifier_cours.html', {
        'cours': cours,
    })


@login_required(login_url='login')
def creer_session_cours(request, cours_id):
    """Créer une session de cours en ligne"""
    from apps.utilisateurs.models_formation import Cours, SessionCoursEnLigne
    from django.utils import timezone
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    cours = get_object_or_404(Cours, pk=cours_id, actif=True)
    
    # Vérifier que l'enseignant est propriétaire
    if cours.enseignant != request.user and request.user not in cours.co_enseignants.all():
        messages.error(request, "Vous n'avez pas le droit de créer une session pour ce cours.")
        return redirect('mes_cours_enseignant')
    
    if request.method == 'POST':
        from django.utils.dateparse import parse_datetime
        session = SessionCoursEnLigne.objects.create(
            cours=cours,
            enseignant=request.user,
            titre=request.POST.get('titre'),
            description=request.POST.get('description', ''),
            date_debut_prevue=parse_datetime(request.POST.get('date_debut_prevue')),
            date_fin_prevue=parse_datetime(request.POST.get('date_fin_prevue')),
            lien_session=request.POST.get('lien_session', ''),
            contenu_session=request.POST.get('contenu_session', ''),
            statut='planifiee'
        )
        messages.success(request, "Session de cours créée avec succès.")
        return redirect('session_cours_detail', session_id=session.id)
    
    return render(request, 'enseignant/creer_session_cours.html', {
        'cours': cours,
    })


@login_required(login_url='login')
def session_cours_detail(request, session_id):
    """Détail d'une session de cours en ligne"""
    from apps.utilisateurs.models_formation import SessionCoursEnLigne
    
    session = get_object_or_404(SessionCoursEnLigne, pk=session_id)
    
    # Vérifier les permissions
    if request.user.est_enseignant():
        if session.enseignant != request.user:
            messages.error(request, "Vous n'avez pas accès à cette session.")
            return redirect('dashboard_enseignant')
    elif request.user.est_etudiant():
        peut_rejoindre, message = session.peut_rejoindre(request.user)
        if not peut_rejoindre:
            messages.error(request, message)
            return redirect('dashboard_etudiant')
    
    return render(request, 'enseignant/session_cours_detail.html', {
        'session': session,
    })


@login_required(login_url='login')
def demarrer_session_cours(request, session_id):
    """Démarrer une session de cours en ligne"""
    from apps.utilisateurs.models_formation import SessionCoursEnLigne
    from django.utils import timezone
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    session = get_object_or_404(SessionCoursEnLigne, pk=session_id)
    
    if session.enseignant != request.user:
        messages.error(request, "Vous n'avez pas le droit de démarrer cette session.")
        return redirect('dashboard_enseignant')
    
    if session.statut == 'planifiee':
        session.statut = 'en_cours'
        session.date_debut_reelle = timezone.now()
        session.save()
        messages.success(request, "Session démarrée avec succès.")
    else:
        messages.warning(request, "La session n'est pas dans un état permettant de la démarrer.")
    
    return redirect('session_cours_detail', session_id=session.id)


@login_required(login_url='login')
def creer_session_evaluation(request, evaluation_id):
    """Créer une session d'évaluation en ligne"""
    from apps.evaluations.models import Evaluation
    from apps.utilisateurs.models_formation import SessionEvaluationEnLigne
    from django.utils import timezone
    from django.utils.dateparse import parse_datetime
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    evaluation = get_object_or_404(Evaluation, pk=evaluation_id, actif=True)
    
    # Vérifier que l'enseignant est propriétaire du cours
    if evaluation.cours.enseignant != request.user and request.user not in evaluation.cours.co_enseignants.all():
        messages.error(request, "Vous n'avez pas le droit de créer une session pour cette évaluation.")
        return redirect('dashboard_enseignant')
    
    if request.method == 'POST':
        session = SessionEvaluationEnLigne.objects.create(
            evaluation=evaluation,
            enseignant=request.user,
            titre=request.POST.get('titre'),
            description=request.POST.get('description', ''),
            date_debut_prevue=parse_datetime(request.POST.get('date_debut_prevue')),
            date_fin_prevue=parse_datetime(request.POST.get('date_fin_prevue')),
            instructions=request.POST.get('instructions', ''),
            statut='planifiee'
        )
        messages.success(request, "Session d'évaluation créée avec succès.")
        return redirect('session_evaluation_detail', session_id=session.id)
    
    return render(request, 'enseignant/creer_session_evaluation.html', {
        'evaluation': evaluation,
    })


@login_required(login_url='login')
def session_evaluation_detail(request, session_id):
    """Détail d'une session d'évaluation en ligne"""
    from apps.utilisateurs.models_formation import SessionEvaluationEnLigne
    from apps.evaluations.models_questionnaire import ParticipationSession
    
    session = get_object_or_404(SessionEvaluationEnLigne, pk=session_id)
    participation = None
    participations = None
    
    # Vérifier les permissions
    if request.user.est_enseignant():
        if session.enseignant != request.user:
            messages.error(request, "Vous n'avez pas accès à cette session.")
            return redirect('dashboard_enseignant')
        
        # Récupérer les participations
        participations = ParticipationSession.objects.filter(session_evaluation=session)
    elif request.user.est_etudiant():
        peut_rejoindre, message = session.peut_rejoindre(request.user)
        if not peut_rejoindre:
            messages.error(request, message)
            return redirect('dashboard_etudiant')
        
        # Créer ou récupérer la participation
        participation, created = ParticipationSession.objects.get_or_create(
            session_evaluation=session,
            etudiant=request.user
        )
        
        # Ajouter l'étudiant aux connectés si pas encore verrouillé
        if not session.verrouillee:
            session.ajouter_etudiant_connecte(request.user)
    else:
        messages.error(request, "Accès non autorisé.")
        return redirect('accueil')
    
    return render(request, 'enseignant/session_evaluation_detail.html', {
        'session': session,
        'participations': participations,
        'participation': participation,
    })


@login_required(login_url='login')
def demarrer_session_evaluation(request, session_id):
    """Démarrer une session d'évaluation et verrouiller l'accès"""
    from apps.utilisateurs.models_formation import SessionEvaluationEnLigne
    from apps.evaluations.models_questionnaire import ParticipationSession
    from django.utils import timezone
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    session = get_object_or_404(SessionEvaluationEnLigne, pk=session_id)
    
    if session.enseignant != request.user:
        messages.error(request, "Vous n'avez pas le droit de démarrer cette session.")
        return redirect('dashboard_enseignant')
    
    if session.statut in ['planifiee', 'en_attente']:
        # Enregistrer les étudiants actuellement connectés
        participations_actives = ParticipationSession.objects.filter(
            session_evaluation=session,
            en_cours=True
        )
        for participation in participations_actives:
            session.etudiants_connectes.add(participation.etudiant)
        
        # Démarrer la session (verrouille automatiquement)
        session.demarrer()
        messages.success(request, "Session d'évaluation démarrée. L'accès est maintenant verrouillé pour les étudiants non connectés.")
    else:
        messages.warning(request, "La session n'est pas dans un état permettant de la démarrer.")
    
    return redirect('session_evaluation_detail', session_id=session.id)


@login_required(login_url='login')
def rejoindre_session_evaluation(request, session_id):
    """Rejoindre une session d'évaluation (étudiant)"""
    from apps.utilisateurs.models_formation import SessionEvaluationEnLigne
    from apps.evaluations.models_questionnaire import ParticipationSession, Question
    from django.utils import timezone
    
    if not request.user.est_etudiant():
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    session = get_object_or_404(SessionEvaluationEnLigne, pk=session_id)
    
    # Vérifier si l'étudiant peut rejoindre
    peut_rejoindre, message = session.peut_rejoindre(request.user)
    if not peut_rejoindre:
        messages.error(request, message)
        return redirect('dashboard_etudiant')
    
    # Créer ou récupérer la participation
    participation, created = ParticipationSession.objects.get_or_create(
        session_evaluation=session,
        etudiant=request.user
    )
    
    if created:
        participation.date_connexion = timezone.now()
        participation.save()
        session.ajouter_etudiant_connecte(request.user)
    
    # Récupérer les questions
    questions = Question.objects.filter(
        evaluation=session.evaluation,
        actif=True
    ).order_by('ordre')
    
    return render(request, 'etudiant/session_evaluation.html', {
        'session': session,
        'participation': participation,
        'questions': questions,
    })


@login_required(login_url='login')
def mes_evaluations_enseignant(request):
    """Liste des évaluations de l'enseignant"""
    from apps.evaluations.models import Evaluation
    from apps.utilisateurs.models_formation import Cours
    
    # Les superutilisateurs ont accès à tout
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    user = request.user
    
    # Récupérer les cours de l'enseignant
    cours_ids = Cours.objects.filter(
        models.Q(enseignant=user) | models.Q(co_enseignants=user)
    ).values_list('id', flat=True)
    
    # Récupérer les évaluations de ces cours
    evaluations = Evaluation.objects.filter(
        cours__in=cours_ids,
        actif=True
    ).order_by('-date_evaluation')
    
    return render(request, 'enseignant/mes_evaluations.html', {
        'evaluations': evaluations,
    })

# Fonction helper pour vérifier l'inscription à une formation
def est_inscrit_formation(user, formation_nom):
    """Vérifie si un utilisateur est inscrit à une formation"""
    if not user.is_authenticated:
        return False
    try:
        from apps.extras.models import FormationExtra, InscriptionExtra
        formation = FormationExtra.objects.filter(titre=formation_nom).first()
        if not formation:
            return False
        return InscriptionExtra.objects.filter(
            utilisateur=user,
            formation=formation,
            valide=True
        ).exists()
    except:
        return False

# === Formations certifiantes ===
@login_required(login_url='login')
def desmfmc(request):
    context = {
        'formation_slug': 'desmfmc',
        'est_inscrit': est_inscrit_formation(request.user, 'DESMFMC')
    }
    return render(request, "formations/desmfmc.html", context)

# Vue publique pour programme/desmfmc/ (accessible sans authentification)
def desmfmc_public(request):
    """Vue publique pour afficher les informations sur le programme DESMFMC sans authentification"""
    # Cette vue est accessible sans authentification
    # Pas de décorateur @login_required
    # Récupérer les informations de coût depuis le modèle
    cout_formation = None
    montant_converti = None
    
    try:
        cout_formation = CoutFormation.objects.get(formation_slug='desmfmc', actif=True)
        # Convertir le montant selon la localisation
        if cout_formation:
            ip_address = get_client_ip(request)
            montant_converti = convertir_montant(cout_formation.get_cout_principal_calcule(), ip_address=ip_address)
    except CoutFormation.DoesNotExist:
        pass
    
    context = {
        'formation_slug': 'desmfmc',
        'est_inscrit': est_inscrit_formation(request.user, 'DESMFMC') if request.user.is_authenticated else False,
        'cout_formation': cout_formation,
        'montant_converti': montant_converti
    }
    return render(request, "programme/desmfmc.html", context)

@login_required(login_url='login')
def sante_communautaire(request):
    context = {
        'formation_slug': 'sante-communautaire',
        'est_inscrit': est_inscrit_formation(request.user, 'Santé Communautaire')
    }
    return render(request, "formations/sante_communautaire.html", context)

# Vue publique pour programme/sante_communautaire/ (accessible sans authentification)
def sante_communautaire_public(request):
    """Vue publique pour afficher les informations sur le programme de santé communautaire sans authentification"""
    # Récupérer les informations de coût depuis le modèle
    cout_formation = None
    montant_converti = None
    
    try:
        cout_formation = CoutFormation.objects.get(formation_slug='sante-communautaire', actif=True)
        # Convertir les montants selon la localisation
        if cout_formation:
            ip_address = get_client_ip(request)
            # Pour les formations avec plusieurs niveaux, convertir chaque montant
            if cout_formation.a_plusieurs_niveaux:
                montant_converti = {}
                if cout_formation.cout_diu:
                    montant_converti['diu'] = convertir_montant(cout_formation.cout_diu, ip_address=ip_address)
                if cout_formation.cout_licence:
                    montant_converti['licence'] = convertir_montant(cout_formation.cout_licence, ip_address=ip_address)
                if cout_formation.cout_master:
                    montant_converti['master'] = convertir_montant(cout_formation.cout_master, ip_address=ip_address)
            else:
                montant_converti = convertir_montant(cout_formation.get_cout_principal_calcule(), ip_address=ip_address)
    except CoutFormation.DoesNotExist:
        pass
    
    context = {
        'formation_slug': 'sante-communautaire',
        'est_inscrit': est_inscrit_formation(request.user, 'Santé Communautaire') if request.user.is_authenticated else False,
        'cout_formation': cout_formation,
        'montant_converti': montant_converti
    }
    return render(request, "programme/sante_communautaire.html", context)

@login_required(login_url='login')
def recherche(request):
    context = {
        'formation_slug': 'recherche',
        'est_inscrit': est_inscrit_formation(request.user, 'Recherche')
    }
    return render(request, "formations/recherche.html", context)

# Vue publique pour programme/recherche/ (accessible sans authentification)
def recherche_public(request):
    """Vue publique pour afficher les informations sur le programme de recherche sans authentification"""
    # Récupérer les informations de coût depuis le modèle
    cout_formation = None
    montant_converti = None
    
    try:
        cout_formation = CoutFormation.objects.get(formation_slug='recherche', actif=True)
        # Convertir le montant selon la localisation
        if cout_formation:
            ip_address = get_client_ip(request)
            montant_converti = convertir_montant(cout_formation.get_cout_principal_calcule(), ip_address=ip_address)
    except CoutFormation.DoesNotExist:
        pass
    
    context = {
        'formation_slug': 'recherche',
        'est_inscrit': est_inscrit_formation(request.user, 'Recherche') if request.user.is_authenticated else False,
        'cout_formation': cout_formation,
        'montant_converti': montant_converti
    }
    return render(request, "programme/recherche.html", context)

@login_required(login_url='login')
def logiciels_analyse_certif(request):
    context = {
        'formation_slug': 'logiciels-analyse',
        'est_inscrit': est_inscrit_formation(request.user, 'Logiciels d\'analyse')
    }
    return render(request, "formations/logiciels_analyse_certif.html", context)

# Vue publique pour programme/logiciels-analyse/ (accessible sans authentification)
def logiciels_analyse_public(request):
    """Vue publique pour afficher les informations sur la formation en logiciels d'analyse sans authentification"""
    # Récupérer les informations de coût depuis le modèle
    cout_formation = None
    montant_converti = None
    
    try:
        cout_formation = CoutFormation.objects.get(formation_slug='logiciels-analyse', actif=True)
        # Convertir le montant selon la localisation
        if cout_formation:
            ip_address = get_client_ip(request)
            montant_converti = convertir_montant(cout_formation.get_cout_principal_calcule(), ip_address=ip_address)
    except CoutFormation.DoesNotExist:
        pass
    
    context = {
        'formation_slug': 'logiciels-analyse',
        'est_inscrit': est_inscrit_formation(request.user, 'Logiciels d\'analyse') if request.user.is_authenticated else False,
        'cout_formation': cout_formation,
        'montant_converti': montant_converti
    }
    return render(request, "programme/logiciels_analyse.html", context)

@login_required(login_url='login')
def echographie_base(request):
    context = {
        'formation_slug': 'echographie-base',
        'est_inscrit': est_inscrit_formation(request.user, 'Échographie de base') if request.user.is_authenticated else False
    }
    return render(request, "formations/echographie_base.html", context)

# Vue publique pour programme/echographie-base/ (accessible sans authentification)
def echographie_base_public(request):
    """Vue publique pour afficher les informations sur la formation en échographie de première ligne sans authentification"""
    # Récupérer les informations de coût depuis le modèle
    cout_formation = None
    montant_converti = None
    
    try:
        cout_formation = CoutFormation.objects.get(formation_slug='echographie-base', actif=True)
        # Convertir le montant selon la localisation
        if cout_formation:
            ip_address = get_client_ip(request)
            montant_converti = convertir_montant(cout_formation.get_cout_principal_calcule(), ip_address=ip_address)
    except CoutFormation.DoesNotExist:
        pass
    
    context = {
        'formation_slug': 'echographie-base',
        'est_inscrit': est_inscrit_formation(request.user, 'Échographie de base') if request.user.is_authenticated else False,
        'cout_formation': cout_formation,
        'montant_converti': montant_converti
    }
    return render(request, "programme/echographie_base.html", context)

@login_required(login_url='login')
def pedagogie_sante(request):
    context = {
        'formation_slug': 'pedagogie-sante',
        'est_inscrit': est_inscrit_formation(request.user, 'Pédagogie en santé')
    }
    return render(request, "formations/pedagogie_sante.html", context)

# Vue publique pour programme/pedagogie-sante/ (accessible sans authentification)
def pedagogie_sante_public(request):
    """Vue publique pour afficher les informations sur le programme de pédagogie sans authentification"""
    # Récupérer les informations de coût depuis le modèle
    cout_formation = None
    montant_converti = None
    
    try:
        cout_formation = CoutFormation.objects.get(formation_slug='pedagogie-sante', actif=True)
        # Convertir le montant selon la localisation
        if cout_formation:
            ip_address = get_client_ip(request)
            montant_converti = convertir_montant(cout_formation.get_cout_principal_calcule(), ip_address=ip_address)
    except CoutFormation.DoesNotExist:
        pass
    
    context = {
        'formation_slug': 'pedagogie-sante',
        'est_inscrit': est_inscrit_formation(request.user, 'Pédagogie en santé') if request.user.is_authenticated else False,
        'cout_formation': cout_formation,
        'montant_converti': montant_converti
    }
    return render(request, "programme/pedagogie_sante.html", context)

# === Formations non certifiantes (accessibles sans authentification) ===
def autres_programmes(request):
    return render(request, "formations/autres_programmes.html")

def logiciels_analyse_noncertif(request):
    context = {
        'formation_slug': 'logiciels-analyse-noncertif',
        'est_inscrit': est_inscrit_formation(request.user, 'Logiciels d\'analyse (Non certifiant)') if request.user.is_authenticated else False
    }
    return render(request, "formations/logiciels_analyse_noncertif.html", context)

def base_pedagogie(request):
    context = {
        'formation_slug': 'base-pedagogie',
        'est_inscrit': est_inscrit_formation(request.user, 'Base en pédagogie') if request.user.is_authenticated else False
    }
    return render(request, "formations/base_pedagogique.html", context)

def cours_med6(request):
    from apps.utilisateurs.forms_med6 import LoginMed6Form
    from core.views_med6 import a_acces_gratuit_med6
    
    # Si l'utilisateur est déjà connecté et est étudiant Med 6, rediriger vers ses cours
    if request.user.is_authenticated and a_acces_gratuit_med6(request.user):
        return redirect('mes_cours')
    
    # Gérer le formulaire de connexion Med 6
    form = LoginMed6Form()
    if request.method == 'POST':
        form = LoginMed6Form(request.POST)
        if form.is_valid():
            etudiant = form.cleaned_data['etudiant']
            
            # Utiliser la même logique que login_med6 pour créer/connecter l'utilisateur
            from apps.utilisateurs.models_med6 import EtudiantMed6
            from apps.utilisateurs.models import Utilisateur
            from django.contrib.auth import login
            import secrets
            import string
            
            if etudiant.utilisateur:
                user = etudiant.utilisateur
            else:
                # Créer un compte utilisateur automatiquement
                base_username = f"med6_{etudiant.matricule.lower().replace(' ', '_')}"
                username = base_username
                counter = 1
                
                while Utilisateur.objects.filter(username=username).exists():
                    username = f"{base_username}_{counter}"
                    counter += 1
                
                password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                
                user = Utilisateur.objects.create_user(
                    username=username,
                    email=f"{username}@med6.fmos-mfmc.ml",
                    password=password,
                    first_name=etudiant.prenom,
                    last_name=etudiant.nom,
                    type_utilisateur='etudiant',
                    classe='Médecine 6',
                    email_verifie=True,
                    is_active=True
                )
                
                etudiant.utilisateur = user
                etudiant.save()
                
                # Créer automatiquement les progressions pour tous les cours Med 6 disponibles
                from apps.utilisateurs.models_formation import Classe, Cours, ProgressionEtudiant
                try:
                    classe_med6 = Classe.objects.filter(nom__icontains='Médecine 6').first()
                    if classe_med6:
                        cours_med6 = Cours.objects.filter(classe=classe_med6, actif=True)
                        for cours in cours_med6:
                            ProgressionEtudiant.objects.get_or_create(
                                etudiant=user,
                                cours=cours,
                                defaults={'statut': 'non_commence'}
                            )
                except:
                    pass
            
            # Connecter l'utilisateur
            login(request, user)
            messages.success(
                request,
                f"Bienvenue {etudiant.nom_complet()} ! Vous avez accès gratuit et automatique à tous les cours de Médecine 6 "
                f"(réservés aux étudiants en 6ème année de médecine)."
            )
            
            return redirect('mes_cours')
    
    # Vérifier si l'utilisateur connecté a accès Med6
    a_acces_gratuit_med6 = False
    if request.user.is_authenticated:
        from core.views_med6 import a_acces_gratuit_med6 as check_acces
        a_acces_gratuit_med6 = check_acces(request.user)
    
    context = {
        'formation_slug': 'cours-med6',
        'est_inscrit': est_inscrit_formation(request.user, 'Cours Médecine 6') if request.user.is_authenticated else False,
        'form': form,
        'a_acces_gratuit_med6': a_acces_gratuit_med6,
    }
    return render(request, "formations/cours_med6.html", context)

def habilites_cliniques(request):
    context = {
        'formation_slug': 'habilites-cliniques',
        'est_inscrit': est_inscrit_formation(request.user, 'Habilités Cliniques') if request.user.is_authenticated else False
    }
    return render(request, "formations/habilites_cliniques.html", context)

def pedagogie(request):
    return render(request, "programme/pedagogie.html")

# Vue pour l'inscription générale avec sélection multiple de formations
@login_required(login_url='login')
def inscription_formations(request, formation_slug=None):
    """
    Vue pour s'inscrire à une ou plusieurs formations avec calcul du coût total.
    L'inscription est soumise à validation par l'administration.
    
    Args:
        formation_slug: Optionnel - slug de la formation à pré-sélectionner
    """
    from apps.extras.models import FormationExtra, InscriptionExtra, PaiementExtra
    from apps.extras.forms import InscriptionMultiFormationForm
    
    # Mapping des slugs vers les noms de formations
    formations_map = {
        'desmfmc': 'DESMFMC',
        'sante-communautaire': 'Santé Communautaire',
        'recherche': 'Recherche',
        'logiciels-analyse': 'Logiciels d\'analyse',
        'echographie-base': 'Échographie de base',
        'pedagogie-sante': 'Pédagogie en santé',
        'cours-med6': 'Cours Médecine 6',
        'habilites-cliniques': 'Habilités Cliniques',
        'logiciels-analyse-noncertif': 'Logiciels d\'analyse (Non certifiant)',
        'base-pedagogie': 'Base en pédagogie',
    }
    
    # Formation à pré-sélectionner
    formation_pre_selectionnee = None
    if formation_slug:
        formation_nom = formations_map.get(formation_slug)
        if formation_nom:
            try:
                formation_pre_selectionnee = FormationExtra.objects.filter(
                    titre=formation_nom, 
                    actif=True
                ).first()
            except:
                pass
    
    if request.method == 'POST':
        form = InscriptionMultiFormationForm(request.POST)
        if form.is_valid():
            try:
                formations_selectionnees = form.cleaned_data['formations']
                mode_paiement = form.cleaned_data.get('mode_paiement', 'bancaire')
                reference_paiement = form.cleaned_data.get('reference_paiement', '')
                
                inscriptions_creees = []
                montant_total = 0
                
                # Créer une inscription pour chaque formation sélectionnée
                for formation in formations_selectionnees:
                    # Vérifier si déjà inscrit
                    inscription_existante = InscriptionExtra.objects.filter(
                        utilisateur=request.user,
                        formation=formation
                    ).first()
                    
                    if inscription_existante:
                        continue  # Passer à la suivante si déjà inscrit
                    
                    # Créer l'inscription (toujours en attente de validation)
                    inscription = InscriptionExtra.objects.create(
                        utilisateur=request.user,
                        formation=formation,
                        valide=False  # En attente de validation par l'admin
                    )
                    inscriptions_creees.append(inscription)
                    montant_total += float(formation.prix)
                    
                    # Créer le paiement si la formation est payante
                    if formation.tarification == 'payante' and formation.prix > 0:
                        PaiementExtra.objects.create(
                            inscription_extra=inscription,
                            montant=formation.prix,
                            mode_paiement=mode_paiement,
                            reference_paiement=reference_paiement,
                            valide=False  # À valider après vérification
                        )
                
                if inscriptions_creees:
                    noms_formations = ', '.join([ins.formation.titre for ins in inscriptions_creees])
                    if montant_total > 0:
                        messages.success(
                            request,
                            f"Votre demande d'inscription à {len(inscriptions_creees)} formation(s) a été soumise avec succès ! "
                            f"Coût total: {montant_total:.0f} FCFA. "
                            f"Votre inscription sera validée par l'administration après vérification. "
                            f"Formations: {noms_formations}"
                        )
                    else:
                        messages.success(
                            request,
                            f"Votre demande d'inscription à {len(inscriptions_creees)} formation(s) a été soumise avec succès ! "
                            f"Votre inscription sera validée par l'administration. "
                            f"Formations: {noms_formations}"
                        )
                else:
                    messages.warning(request, "Vous êtes déjà inscrit à toutes les formations sélectionnées.")
                
                return redirect('mes_formations')
                
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de l'inscription: {str(e)}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        # Initialiser le formulaire avec la formation pré-sélectionnée si fournie
        initial_data = {}
        if formation_pre_selectionnee:
            initial_data = {'formations': [formation_pre_selectionnee.id]}
        form = InscriptionMultiFormationForm(initial=initial_data)
    
    # Récupérer toutes les formations actives avec leurs prix pour le JavaScript
    formations_actives = FormationExtra.objects.filter(actif=True).order_by('titre')
    
    import json
    formations_data = json.dumps([
        {'id': f.id, 'titre': f.titre, 'prix': float(f.prix), 'gratuite': f.tarification == 'gratuite' or f.prix == 0}
        for f in formations_actives
    ])
    
    context = {
        'form': form,
        'formations': formations_actives,
        'formations_data': formations_data,
        'formation_pre_selectionnee_id': formation_pre_selectionnee.id if formation_pre_selectionnee else None,
    }
    
    return render(request, 'formations/inscription_multi.html', context)

# Vue pour gérer l'inscription aux formations (ancien système - conservé pour compatibilité)
@login_required(login_url='login')
def inscrire_formation(request, formation_slug):
    """
    Vue pour s'inscrire à une formation avec formulaire de paiement.
    formation_slug: identifiant de la formation (ex: 'desmfmc', 'recherche', etc.)
    """
    from apps.extras.models import FormationExtra, InscriptionExtra, PaiementExtra
    from apps.extras.forms import InscriptionFormationForm
    from datetime import date, timedelta
    
    # Mapping des formations vers leurs noms et coûts par défaut
    formations_map = {
        'desmfmc': {'nom': 'DESMFMC', 'prix': 0.00},
        'sante-communautaire': {'nom': 'Santé Communautaire', 'prix': 0.00},
        'recherche': {'nom': 'Recherche', 'prix': 0.00},
        'logiciels-analyse': {'nom': 'Logiciels d\'analyse', 'prix': 0.00},
        'echographie-base': {'nom': 'Échographie de base', 'prix': 0.00},
        'pedagogie-sante': {'nom': 'Pédagogie en santé', 'prix': 0.00},
        'cours-med6': {'nom': 'Cours Médecine 6', 'prix': 0.00},
        'habilites-cliniques': {'nom': 'Habilités Cliniques', 'prix': 0.00},
        'logiciels-analyse-noncertif': {'nom': 'Logiciels d\'analyse (Non certifiant)', 'prix': 0.00},
        'base-pedagogie': {'nom': 'Base en pédagogie', 'prix': 0.00},
    }
    
    formation_info = formations_map.get(formation_slug)
    
    if not formation_info:
        messages.error(request, "Formation introuvable.")
        return redirect('formations')
    
    formation_nom = formation_info['nom']
    prix_par_defaut = formation_info['prix']
    
    # Chercher ou créer la formation
    formation, created = FormationExtra.objects.get_or_create(
        titre=formation_nom,
        defaults={
            'description': f'Formation: {formation_nom}',
            'type_formation': 'certifiante' if 'certifiant' in formation_slug.lower() or formation_slug in ['desmfmc', 'recherche', 'logiciels-analyse', 'echographie-base', 'pedagogie-sante'] else 'non_certifiante',
            'tarification': 'gratuite' if prix_par_defaut == 0 else 'payante',
            'prix': prix_par_defaut,
            'date_debut': date.today(),
            'date_fin': date.today() + timedelta(days=365),
            'actif': True
        }
    )
    
    # Vérifier si déjà inscrit
    inscription_existante = InscriptionExtra.objects.filter(
        utilisateur=request.user,
        formation=formation
    ).first()
    
    if inscription_existante:
        messages.info(request, f"Vous êtes déjà inscrit à la formation '{formation_nom}'.")
        return redirect('mes_formations')
    
    # Traitement du formulaire
    est_payante = formation.tarification == 'payante' and formation.prix > 0
    
    if request.method == 'POST':
        form = InscriptionFormationForm(request.POST, est_payante=est_payante)
        if form.is_valid():
            try:
                # Créer l'inscription
                inscription = InscriptionExtra.objects.create(
                    utilisateur=request.user,
                    formation=formation,
                    valide=False  # En attente de validation du paiement
                )
                
                # Créer le paiement si la formation est payante
                if est_payante:
                    mode_paiement = form.cleaned_data.get('mode_paiement', 'bancaire')
                    paiement = PaiementExtra.objects.create(
                        inscription_extra=inscription,
                        montant=formation.prix,
                        mode_paiement=mode_paiement,
                        reference_paiement=form.cleaned_data.get('reference_paiement', ''),
                        valide=False  # À valider après vérification du paiement
                    )
                    messages.success(
                        request,
                        f"Inscription enregistrée ! Votre paiement de {formation.prix} FCFA sera validé après vérification. "
                        f"Référence: {paiement.reference_paiement or 'À compléter'}"
                    )
                else:
                    # Formation gratuite, inscription validée directement
                    inscription.valide = True
                    inscription.save()
                    messages.success(request, f"Vous êtes maintenant inscrit à la formation '{formation_nom}'.")
                
                return redirect('mes_formations')
                
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de l'inscription: {str(e)}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = InscriptionFormationForm(est_payante=est_payante)
    
    # Contexte pour le template
    context = {
        'formation': formation,
        'formation_nom': formation_nom,
        'formation_slug': formation_slug,
        'form': form,
        'prix': formation.prix,
        'est_gratuite': formation.tarification == 'gratuite' or formation.prix == 0,
    }
    
    return render(request, 'formations/inscription_form.html', context)

# Vue pour afficher les formations de l'utilisateur
@login_required(login_url='login')
def mes_formations(request):
    """Affiche les formations auxquelles l'utilisateur est inscrit"""
    try:
        from apps.extras.models import InscriptionExtra
        
        inscriptions = InscriptionExtra.objects.filter(
            utilisateur=request.user,
            valide=True
        ).select_related('formation')
        
        context = {
            'inscriptions': inscriptions
        }
        return render(request, "formations/mes_formations.html", context)
    except Exception as e:
        messages.error(request, f"Une erreur est survenue: {str(e)}")
        return redirect('formations')

# Note: Les vues desmfmc, sante_communautaire, etc. pour formations/ sont définies plus haut
# avec @login_required et utilisent les templates formations/*.html
# Ces fonctions ci-dessous sont pour les routes programme/ (si nécessaire)
# Elles sont commentées pour éviter les conflits avec les vues formations/

# def desmfmc_programme(request):
#     return render(request, "programme/desmfmc.html")

# def sante_communautaire_programme(request):
#     return render(request, "programme/sante_communautaire.html")

# def recherche_programme(request):
#     return render(request, "programme/recherche.html")

# def echographie_base_programme(request):
#     return render(request, "programme/echographie_base.html")

# Les fonctions pedagogie_sante et autres_programmes sont déjà définies plus haut
# avec @login_required et utilisent les templates formations/*.html
# Ces définitions en double sont supprimées pour éviter les conflits


# === Handlers d'erreurs ===
def custom_404(request, exception):
    return render(request, "404.html", status=404)

def custom_500(request):
    return render(request, "500.html", status=500)
