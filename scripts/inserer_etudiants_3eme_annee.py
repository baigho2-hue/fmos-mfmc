#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour insérer des étudiants en 3ème année du DESMFMC dans la base de données.
Utilise l'email comme username et le mot de passe "etudiant123".
Crée les ResultatAnneeDES nécessaires pour les années 1 et 2 (statut 'admis').

Usage:
    python scripts/inserer_etudiants_3eme_annee.py
"""
import os
import sys
from decimal import Decimal

# Configurer l'encodage pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Ajouter le répertoire racine du projet au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from django.utils import timezone
from django.contrib.auth.hashers import make_password

from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Formation, Classe
from apps.utilisateurs.models_programme_desmfmc import ResultatAnneeDES


# Liste des étudiants à insérer
ETUDIANTS = [
    {
        'nom': 'Camara',
        'prenom': 'Aboubacar',
        'telephone': '66045707',
        'email': 'Boubacarc8@gmail.com',
    },
    {
        'nom': 'Kané',
        'prenom': 'Mariam',
        'telephone': '76174702',
        'email': 'marikan@yahoo.fr',
    },
    {
        'nom': 'Dicko',
        'prenom': 'Oumar',
        'telephone': '76359148',
        'email': 'Oumardicko735@gmail.com',
    },
    {
        'nom': 'Baré',
        'prenom': 'Mathieu',
        'telephone': '78855036',
        'email': 'mbare1032@gmail.com',
    },
]

PASSWORD = 'etudiant123'
CLASSE_NOM = '3ème A'
ANNEE_ACTUELLE = 3


def trouver_formation_desmfmc():
    """Trouve la formation DESMFMC."""
    formation = Formation.objects.filter(code='DESMFMC', actif=True).first()
    if not formation:
        raise SystemExit("❌ Formation DESMFMC introuvable ou inactive.")
    return formation


def trouver_classe_3eme_annee(formation):
    """Trouve la classe 3ème A pour le DESMFMC."""
    # Chercher d'abord par nom exact
    classe = Classe.objects.filter(
        formation=formation,
        nom__icontains='3ème A',
        actif=True
    ).first()
    
    # Si pas trouvé, chercher par année 3
    if not classe:
        classe = Classe.objects.filter(
            formation=formation,
            annee=3,
            actif=True
        ).first()
    
    if not classe:
        raise SystemExit(f"❌ Classe '{CLASSE_NOM}' ou classe année 3 introuvable pour DESMFMC.")
    
    return classe


def creer_ou_mettre_a_jour_etudiant(etudiant_data, formation, classe):
    """Crée ou met à jour un étudiant."""
    email = etudiant_data['email'].strip()
    username = email  # Utiliser l'email comme username
    
    # Vérifier si l'utilisateur existe déjà
    utilisateur = Utilisateur.objects.filter(
        email__iexact=email
    ).first() or Utilisateur.objects.filter(
        username__iexact=username
    ).first()
    
    if utilisateur:
        print(f"  ⚠️  Étudiant existant trouvé: {utilisateur.username}")
        # Mettre à jour les informations
        utilisateur.first_name = etudiant_data['prenom']
        utilisateur.last_name = etudiant_data['nom']
        utilisateur.telephone = etudiant_data['telephone']
        utilisateur.classe = CLASSE_NOM  # Utiliser "3ème A" comme demandé
        utilisateur.type_utilisateur = 'etudiant'
        utilisateur.email_verifie = True
        utilisateur.is_active = True
        if not utilisateur.date_joined:
            utilisateur.date_joined = timezone.now()
        utilisateur.save()
        print(f"  ✅ Étudiant mis à jour: {utilisateur.get_full_name()}")
        return utilisateur, False
    
    # Créer un nouvel utilisateur
    utilisateur = Utilisateur.objects.create_user(
        username=username,
        email=email,
        password=PASSWORD,
        first_name=etudiant_data['prenom'],
        last_name=etudiant_data['nom'],
        telephone=etudiant_data['telephone'],
        classe=CLASSE_NOM,  # Utiliser "3ème A" comme demandé
        type_utilisateur='etudiant',
        email_verifie=True,
        is_active=True,
        date_joined=timezone.now(),
    )
    print(f"  ✅ Étudiant créé: {utilisateur.get_full_name()} ({username})")
    return utilisateur, True


def creer_resultat_annee(etudiant, formation, annee):
    """Crée le ResultatAnneeDES pour une année avec statut 'admis'."""
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
        etudiant=etudiant,
        formation=formation,
        annee=annee,
        defaults=defaults,
    )
    
    if not cree:
        # Mettre à jour si existe déjà
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


def main():
    """Fonction principale."""
    print("=" * 70)
    print("Insertion des étudiants en 3ème année du DESMFMC")
    print("=" * 70)
    
    # Trouver la formation et la classe
    formation = trouver_formation_desmfmc()
    classe = trouver_classe_3eme_annee(formation)
    
    print(f"\n✅ Formation: {formation.nom}")
    print(f"✅ Classe: {classe.nom} (année {classe.annee})")
    print(f"✅ Mot de passe: {PASSWORD}")
    print(f"\nNombre d'étudiants à traiter: {len(ETUDIANTS)}\n")
    
    stats = {
        'crees': 0,
        'mis_a_jour': 0,
        'resultats_crees': 0,
        'erreurs': 0,
    }
    
    # Traiter chaque étudiant
    for idx, etudiant_data in enumerate(ETUDIANTS, 1):
        print(f"\n[{idx}/{len(ETUDIANTS)}] {etudiant_data['prenom']} {etudiant_data['nom']}")
        
        try:
            # Créer ou mettre à jour l'étudiant
            utilisateur, est_nouveau = creer_ou_mettre_a_jour_etudiant(
                etudiant_data, formation, classe
            )
            
            if est_nouveau:
                stats['crees'] += 1
            else:
                stats['mis_a_jour'] += 1
            
            # Créer les résultats pour les années 1 et 2
            for annee in [1, 2]:
                resultat, cree = creer_resultat_annee(utilisateur, formation, annee)
                if cree:
                    stats['resultats_crees'] += 1
                print(f"  ✅ Résultat année {annee}: {'créé' if cree else 'déjà existant'}")
            
        except Exception as e:
            stats['erreurs'] += 1
            print(f"  ❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
    
    # Récapitulatif
    print("\n" + "=" * 70)
    print("RÉCAPITULATIF")
    print("=" * 70)
    print(f"✅ Étudiants créés: {stats['crees']}")
    print(f"✅ Étudiants mis à jour: {stats['mis_a_jour']}")
    print(f"✅ Résultats années 1 et 2 créés/mis à jour: {stats['resultats_crees']}")
    if stats['erreurs'] > 0:
        print(f"❌ Erreurs: {stats['erreurs']}")
    print("\n✅ Les étudiants peuvent maintenant se connecter avec:")
    print(f"   - Username: leur adresse email")
    print(f"   - Mot de passe: {PASSWORD}")
    print("\n✅ Ils peuvent suivre le processus de validation de passage en classe supérieure.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterruption utilisateur. Aucune modification n'a été effectuée.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

