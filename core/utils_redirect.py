# core/utils_redirect.py
"""
Utilitaires pour la redirection après connexion selon le niveau d'accès
"""
from django.shortcuts import redirect


def get_redirect_after_login(user):
    """
    Détermine la redirection après connexion selon le type et le niveau d'accès de l'utilisateur
    
    Args:
        user: L'utilisateur connecté
        
    Returns:
        Le nom de l'URL vers laquelle rediriger
    """
    # Superutilisateurs -> Admin Django
    if user.is_superuser:
        return 'admin:index'
    
    # Membres de la coordination -> Dashboard administration
    if user.est_membre_coordination():
        return 'dashboard_administration'
    
    # Enseignants -> Dashboard enseignant
    if user.est_enseignant():
        return 'dashboard_enseignant'
    
    # Étudiants -> Dashboard étudiant
    if user.est_etudiant():
        return 'dashboard_etudiant'
    
    # Par défaut -> Accueil
    return 'accueil'

