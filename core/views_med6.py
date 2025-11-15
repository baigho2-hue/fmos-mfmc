# core/views_med6.py
"""
Vues pour l'authentification et l'accès des étudiants Med 6
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.utilisateurs.forms_med6 import LoginMed6Form
from apps.utilisateurs.models_med6 import EtudiantMed6
from apps.utilisateurs.models import Utilisateur
import secrets
import string


def login_med6(request):
    """
    Vue de connexion spéciale pour les étudiants de Médecine 6
    """
    if request.user.is_authenticated:
        # Si déjà connecté, rediriger vers le dashboard
        if request.user.est_etudiant():
            return redirect('dashboard_etudiant')
        else:
            return redirect('accueil')
    
    if request.method == 'POST':
        form = LoginMed6Form(request.POST)
        if form.is_valid():
            etudiant = form.cleaned_data['etudiant']
            
            # Vérifier si un compte utilisateur existe déjà pour cet étudiant
            if etudiant.utilisateur:
                user = etudiant.utilisateur
            else:
                # Créer un compte utilisateur automatiquement
                # Générer un username unique basé sur le matricule
                base_username = f"med6_{etudiant.matricule.lower().replace(' ', '_')}"
                username = base_username
                counter = 1
                
                # S'assurer que le username est unique
                while Utilisateur.objects.filter(username=username).exists():
                    username = f"{base_username}_{counter}"
                    counter += 1
                
                # Générer un mot de passe aléatoire (l'étudiant pourra le changer)
                password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                
                # Créer l'utilisateur avec accès automatique aux cours Med 6
                user = Utilisateur.objects.create_user(
                    username=username,
                    email=f"{username}@med6.fmos-mfmc.ml",  # Email temporaire
                    password=password,
                    first_name=etudiant.prenom,
                    last_name=etudiant.nom,
                    type_utilisateur='etudiant',
                    classe='Médecine 6',
                    email_verifie=True,  # Pas besoin de vérification pour Med 6
                    is_active=True
                )
                
                # Lier l'étudiant Med 6 à l'utilisateur
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
                except Exception as e:
                    # Ignorer les erreurs silencieusement - les progressions seront créées à la demande
                    pass
                
                # Stocker le mot de passe temporaire dans la session pour l'afficher
                request.session['med6_temp_password'] = password
            
            # Connecter l'utilisateur
            login(request, user)
            messages.success(
                request,
                f"Bienvenue {etudiant.nom_complet()} ! Vous avez accès gratuit et automatique à tous les cours de Médecine 6 "
                f"(réservés aux étudiants en 6ème année de médecine). Aucune inscription supplémentaire n'est nécessaire."
            )
            
            # Si c'est un nouveau compte, afficher le mot de passe temporaire
            if 'med6_temp_password' in request.session:
                temp_password = request.session.pop('med6_temp_password')
                messages.info(
                    request,
                    f"Votre mot de passe temporaire est : {temp_password}. "
                    "Nous vous recommandons de le changer dans vos paramètres."
                )
            
            return redirect('dashboard_etudiant')
    else:
        form = LoginMed6Form()
    
    return render(request, 'login_med6.html', {
        'form': form
    })


def est_etudiant_med6(user):
    """
    Vérifie si un utilisateur est un étudiant Med 6 avec accès gratuit
    et que sa liste n'est pas expirée
    
    IMPORTANT: Cette fonction accepte un objet Utilisateur, PAS une requête.
    Ne pas utiliser de décorateur @login_required ici.
    
    Args:
        user: Objet Utilisateur (pas une requête)
    
    Returns:
        bool: True si l'utilisateur est un étudiant Med 6 avec accès valide
    """
    # Vérifier que user est bien un objet Utilisateur et non une requête
    if not user:
        return False
    
    # Vérifier que c'est bien un objet Utilisateur avec is_authenticated
    if not hasattr(user, 'is_authenticated'):
        return False
    
    if not user.is_authenticated:
        return False
    
    try:
        # Accéder à la relation etudiant_med6
        etudiant_med6 = user.etudiant_med6
        if not etudiant_med6:
            return False
        
        if not etudiant_med6.actif:
            return False
        
        # Vérifier que la liste existe
        if not etudiant_med6.liste:
            return False
        
        # Vérifier que la liste n'est pas expirée
        if etudiant_med6.liste.est_expiree():
            return False
        
        # Vérifier que la liste est active
        if not etudiant_med6.liste.active:
            return False
        
        return True
    except AttributeError:
        # L'utilisateur n'a pas de relation etudiant_med6
        return False
    except Exception:
        # Autre erreur
        return False


def a_acces_gratuit_med6(user):
    """
    Vérifie si un utilisateur a accès gratuit aux cours Médecine 6
    
    IMPORTANT: Accès réservé UNIQUEMENT aux étudiants en 6ème année de médecine
    qui sont dans la liste Excel officielle validée (matricule, nom, prénom).
    
    Args:
        user: Objet Utilisateur
    
    Returns:
        bool: True si l'utilisateur est un étudiant de 6ème année avec accès valide
    """
    if not user.is_authenticated:
        return False
    
    # Vérifier si c'est un étudiant Med 6 avec liste valide ET actif
    # C'est la SEULE façon d'obtenir l'accès gratuit
    if est_etudiant_med6(user):
        return True
    
    # IMPORTANT: Ne pas autoriser l'accès simplement parce que la classe contient "Médecine 6"
    # L'accès doit être validé via la liste Excel uniquement
    return False

