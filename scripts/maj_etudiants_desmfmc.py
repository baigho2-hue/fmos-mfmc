#!/usr/bin/env python
"""
Script interactif pour ajouter/mettre à jour manuellement les étudiants DESMFMC
des années 2 à 4. Permet de :
  * associer la bonne classe (DESMFMC année 2/3/4) sur le modèle Utilisateur
  * marquer l'année correspondante comme "admis" dans ResultatAnneeDES

Usage :
    python scripts/maj_etudiants_desmfmc.py

Le script boucle tant que l'on saisit des identifiants d'étudiants.
Appuyer sur Entrée sans rien saisir pour quitter.
"""
import os
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django  # noqa: E402  (import après configuration DJANGO_SETTINGS_MODULE)

django.setup()

from django.utils import timezone  # noqa: E402

from apps.utilisateurs.models import Utilisateur  # noqa: E402
from apps.utilisateurs.models_formation import Formation, Classe  # noqa: E402
from apps.utilisateurs.models_programme_desmfmc import (  # noqa: E402
    ResultatAnneeDES,
)


def charger_formation_et_classes():
    """Retourne la formation DESMFMC et un mapping année -> classe."""
    try:
        formation = Formation.objects.get(code='DESMFMC')
    except Formation.DoesNotExist:
        raise SystemExit(
            "❌ La formation DESMFMC n'existe pas encore. "
            "Lancez les migrations/commandes d'initialisation puis réessayez."
        )

    classes = {}
    for annee in (1, 2, 3, 4):
        classe = Classe.objects.filter(formation=formation, annee=annee, actif=True).first()
        if classe:
            classes[annee] = classe

    if not classes:
        raise SystemExit("❌ Aucune classe DESMFMC active trouvée.")

    return formation, classes


def trouver_utilisateur(identifiant):
    """Recherche par username, email ou id numérique."""
    utilisateur = (
        Utilisateur.objects.filter(username__iexact=identifiant).first()
        or Utilisateur.objects.filter(email__iexact=identifiant).first()
    )

    if utilisateur is None and identifiant.isdigit():
        utilisateur = Utilisateur.objects.filter(id=int(identifiant)).first()

    return utilisateur


def mettre_a_jour_resultat(user, formation, annee):
    """Crée/actualise le ResultatAnneeDES correspondant."""
    resultat, cree = ResultatAnneeDES.objects.get_or_create(
        etudiant=user,
        formation=formation,
        annee=annee,
        defaults={
            'decision': 'admis',
            'cours_theoriques_valides': True,
            'presence_validee': True,
            'stages_valides': True,
            'note_theorique': Decimal('10.00'),
            'note_pratique': Decimal('10.00'),
        },
    )

    # Si déjà existant, on force la décision à "admis"
    if not cree:
        resultat.decision = 'admis'
        resultat.cours_theoriques_valides = True
        resultat.presence_validee = True
        resultat.stages_valides = True
        if resultat.note_theorique is None:
            resultat.note_theorique = Decimal('10.00')
        if resultat.note_pratique is None:
            resultat.note_pratique = Decimal('10.00')
        resultat.save()

    return resultat, cree


def boucle_interactive():
    formation, classes = charger_formation_et_classes()
    print("=== Mise à jour des étudiants DESMFMC (années 2, 3, 4) ===")
    print("Entrer un username / email / id utilisateur. Laisser vide pour quitter.\n")

    stats = {'traites': 0, 'classe_mise_a_jour': 0, 'resultats_maj': 0}

    while True:
        identifiant = input("Identifiant utilisateur: ").strip()
        if not identifiant:
            break

        utilisateur = trouver_utilisateur(identifiant)
        if not utilisateur:
            print(f"  ❌ Utilisateur '{identifiant}' introuvable.\n")
            continue

        if not utilisateur.est_etudiant():
            print("  ⚠️ Utilisateur trouvé mais pas de type 'étudiant'. Ignoré.\n")
            continue

        try:
            annee = int(input("  Année du DES (2, 3 ou 4): ").strip())
        except ValueError:
            print("  ❌ Valeur d'année invalide.\n")
            continue

        if annee not in (2, 3, 4):
            print("  ❌ Seules les années 2, 3 ou 4 sont autorisées.\n")
            continue

        classe = classes.get(annee)
        if not classe:
            print(f"  ❌ Aucune classe active trouvée pour l'année {annee}.\n")
            continue

        stats['traites'] += 1

        # Mise à jour de la classe de l'utilisateur
        if utilisateur.classe != classe.nom:
            utilisateur.classe = classe.nom
            utilisateur.date_joined = utilisateur.date_joined or timezone.now()
            utilisateur.save(update_fields=['classe', 'date_joined'])
            stats['classe_mise_a_jour'] += 1
            print(f"  ✅ Classe mise à jour: {classe.nom}")
        else:
            print("  ℹ️ Classe déjà à jour.")

        # Mise à jour des résultats annuels
        resultat, cree = mettre_a_jour_resultat(utilisateur, formation, annee)
        stats['resultats_maj'] += 1
        print(
            f"  ✅ ResultatAnneeDES {'créé' if cree else 'mis à jour'} "
            f"(année {annee}, décision: {resultat.get_decision_display()})\n"
        )

    print("\n=== Récapitulatif ===")
    print(f"Étudiants traités : {stats['traites']}")
    print(f"Classes mises à jour : {stats['classe_mise_a_jour']}")
    print(f"Résultats annuels créés/mis à jour : {stats['resultats_maj']}")
    print("Fin du script.")


if __name__ == "__main__":
    try:
        boucle_interactive()
    except KeyboardInterrupt:
        print("\nInterruption utilisateur. Rien de plus n'a été fait.")

