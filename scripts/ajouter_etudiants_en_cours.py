#!/usr/bin/env python
"""
Script interactif pour ajouter manuellement des étudiants en cours de formation
avant la création du site. Permet de :
  * créer un utilisateur étudiant
  * l'associer à la bonne classe selon la formation
  * définir l'année d'étude actuelle
  * pour DESMFMC : créer les ResultatAnneeDES pour les années précédentes validées

Usage :
    python scripts/ajouter_etudiants_en_cours.py

Le script boucle tant que l'on saisit des informations d'étudiants.
Appuyer sur Entrée sans rien saisir pour quitter.
"""
import os
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django  # noqa: E402  (import après configuration DJANGO_SETTINGS_MODULE)

django.setup()

from django.utils import timezone  # noqa: E402
from django.contrib.auth.hashers import make_password  # noqa: E402

from apps.utilisateurs.models import Utilisateur  # noqa: E402
from apps.utilisateurs.models_formation import Formation, Classe  # noqa: E402
from apps.utilisateurs.models_programme_desmfmc import (  # noqa: E402
    ResultatAnneeDES,
)


def charger_formations():
    """Retourne un dictionnaire code -> formation."""
    formations = {}
    for formation in Formation.objects.filter(actif=True):
        formations[formation.code] = formation
    return formations


def trouver_ou_creer_utilisateur(username, email, prenom, nom):
    """Trouve un utilisateur existant ou en crée un nouveau."""
    # Chercher par username ou email
    utilisateur = (
        Utilisateur.objects.filter(username__iexact=username).first()
        or Utilisateur.objects.filter(email__iexact=email).first()
    )
    
    if utilisateur:
        print(f"  ⚠️ Utilisateur existant trouvé: {utilisateur.username}")
        reponse = input("  Utiliser cet utilisateur? (o/n): ").strip().lower()
        if reponse != 'o':
            return None
        return utilisateur
    
    # Créer un nouvel utilisateur
    if not username:
        username = email.split('@')[0] if email else f"etudiant_{timezone.now().timestamp()}"
    
    # Générer un mot de passe temporaire
    password = make_password(f"temp_{username}_2024")
    
    utilisateur = Utilisateur.objects.create(
        username=username,
        email=email,
        first_name=prenom,
        last_name=nom,
        password=password,
        type_utilisateur='etudiant',
        is_active=True,
        date_joined=timezone.now(),
    )
    
    print(f"  ✅ Utilisateur créé: {utilisateur.username}")
    return utilisateur


def mettre_a_jour_resultat_des(user, formation, annee):
    """Crée/actualise le ResultatAnneeDES pour une année validée."""
    defaults = {
        'decision': 'admis',
        'decision_forcee': True,
        'cours_theoriques_valides': True,
        'presence_validee': True,
        'stages_valides': True,
        'note_theorique': Decimal('10.00'),
        'note_pratique': Decimal('10.00'),
        'date_decision': timezone.now().date(),
    }
    
    resultat, cree = ResultatAnneeDES.objects.get_or_create(
        etudiant=user,
        formation=formation,
        annee=annee,
        defaults=defaults,
    )
    
    if not cree:
        resultat.decision = 'admis'
        resultat.decision_forcee = True
        resultat.cours_theoriques_valides = True
        resultat.presence_validee = True
        resultat.stages_valides = True
        if resultat.note_theorique is None:
            resultat.note_theorique = Decimal('10.00')
        if resultat.note_pratique is None:
            resultat.note_pratique = Decimal('10.00')
        if resultat.date_decision is None:
            resultat.date_decision = timezone.now().date()
        resultat.save()
    
    return resultat, cree


def boucle_interactive():
    formations = charger_formations()
    
    if not formations:
        raise SystemExit("❌ Aucune formation active trouvée.")
    
    print("=== Ajout d'étudiants en cours de formation ===")
    print("Ce script permet d'ajouter des étudiants qui étaient déjà en formation")
    print("avant la création du site.\n")
    
    stats = {
        'crees': 0,
        'utilises': 0,
        'classes_mises_a_jour': 0,
        'resultats_des_crees': 0
    }
    
    while True:
        print("\n" + "="*60)
        print("Nouvel étudiant (laisser vide pour quitter)")
        
        # Informations de base
        username = input("Username (optionnel, généré automatiquement si vide): ").strip()
        email = input("Email: ").strip()
        if not email:
            break
        
        prenom = input("Prénom: ").strip()
        nom = input("Nom: ").strip()
        
        # Formation
        print("\nFormations disponibles:")
        for code, formation in formations.items():
            print(f"  - {code}: {formation.nom}")
        
        code_formation = input("\nCode de la formation: ").strip().upper()
        if not code_formation:
            print("  ❌ Code de formation requis.")
            continue
        
        formation = formations.get(code_formation)
        if not formation:
            print(f"  ❌ Formation '{code_formation}' introuvable.")
            continue
        
        # Année actuelle
        try:
            annee_actuelle = int(input(f"Année actuelle (1 à {formation.duree_annees}): ").strip())
        except ValueError:
            print("  ❌ Valeur d'année invalide.")
            continue
        
        if annee_actuelle < 1 or annee_actuelle > formation.duree_annees:
            print(f"  ❌ L'année doit être entre 1 et {formation.duree_annees}.")
            continue
        
        # Classe
        classe = Classe.objects.filter(
            formation=formation,
            annee=annee_actuelle,
            actif=True
        ).first()
        
        if not classe:
            print(f"  ❌ Aucune classe active trouvée pour l'année {annee_actuelle}.")
            continue
        
        # Créer ou trouver l'utilisateur
        utilisateur = trouver_ou_creer_utilisateur(username, email, prenom, nom)
        if not utilisateur:
            print("  ❌ Impossible de créer/trouver l'utilisateur.")
            continue
        
        if utilisateur.id:
            stats['utilises'] += 1
        else:
            stats['crees'] += 1
        
        # Mise à jour de la classe
        if utilisateur.classe != classe.nom:
            utilisateur.classe = classe.nom
            utilisateur.date_joined = utilisateur.date_joined or timezone.now()
            utilisateur.save(update_fields=['classe', 'date_joined'])
            stats['classe_mise_a_jour'] += 1
            print(f"  ✅ Classe mise à jour: {classe.nom}")
        else:
            print("  ℹ️ Classe déjà à jour.")
        
        # Pour DESMFMC : créer les résultats pour les années précédentes validées
        if code_formation == 'DESMFMC' and annee_actuelle > 1:
            print(f"\n  Création des résultats pour les années précédentes (1 à {annee_actuelle - 1})...")
            for annee_validee in range(1, annee_actuelle):
                resultat, cree = mettre_a_jour_resultat_des(utilisateur, formation, annee_validee)
                stats['resultats_des_crees'] += 1
                print(f"    ✅ Année {annee_validee}: {'créé' if cree else 'mis à jour'}")
        
        print(f"\n  ✅ Étudiant ajouté/mis à jour: {utilisateur.get_full_name() or utilisateur.username}")
    
    print("\n" + "="*60)
    print("=== Récapitulatif ===")
    print(f"Étudiants créés : {stats['crees']}")
    print(f"Étudiants existants utilisés : {stats['utilises']}")
    print(f"Classes mises à jour : {stats['classe_mise_a_jour']}")
    print(f"Résultats DES créés/mis à jour : {stats['resultats_des_crees']}")
    print("\n⚠️  IMPORTANT: Les étudiants créés ont un mot de passe temporaire.")
    print("   Ils devront utiliser la fonction 'Mot de passe oublié' pour définir leur mot de passe.")
    print("Fin du script.")


if __name__ == "__main__":
    try:
        boucle_interactive()
    except KeyboardInterrupt:
        print("\nInterruption utilisateur. Rien de plus n'a été fait.")

