from django.db import migrations
import datetime
from datetime import time, datetime as dt
from django.utils import timezone


def seed_planifications(apps, schema_editor):
    Formation = apps.get_model('utilisateurs', 'Formation')
    Cours = apps.get_model('utilisateurs', 'Cours')
    Planification = apps.get_model('utilisateurs', 'Planification')
    Classe = apps.get_model('utilisateurs', 'Classe')

    formation = Formation.objects.filter(code='DESMFMC').first()
    if not formation:
        return

    # ------------------------------------------------------------------
    # Planifications issues des cours
    # ------------------------------------------------------------------
    cours_qs = Cours.objects.filter(classe__formation=formation, actif=True)

    current_tz = timezone.get_current_timezone()

    def make_datetime(date_value, default_hour):
        naive = dt.combine(date_value, time(default_hour, 0))
        return timezone.make_aware(naive, current_tz) if timezone.is_naive(naive) else naive

    for cours in cours_qs:
        titre = f"Cours : {cours.titre}"
        debut = make_datetime(cours.date_debut, 8)
        fin = make_datetime(cours.date_fin, 17)
        defaults = {
            'description': cours.description,
            'type_activite': 'cours',
            'date_fin': fin,
            'duree_heures': min(cours.volume_horaire or 0, 999),
            'lieu': cours.classe.formation.nom,
            'cours_lie': cours,
            'actif': True,
        }

        planification, _ = Planification.objects.get_or_create(
            classe=cours.classe,
            titre=titre,
            date_debut=debut,
            defaults=defaults,
        )

        # Mise à jour idempotente
        for field, value in defaults.items():
            setattr(planification, field, value)
        planification.save()

    # ------------------------------------------------------------------
    # Planifications des stages et immersions
    # ------------------------------------------------------------------
    stage_data = {
        'DES-A1': [
            {
                'titre': "Stage Médecine interne - Point G",
                'date_debut': datetime.date(2025, 10, 1),
                'date_fin': datetime.date(2025, 11, 30),
                'description': "Internat rotatoire : immersion en médecine interne (2 mois).",
                'lieu': "CHU Point G",
            },
            {
                'titre': "Stage Chirurgie générale - Point G",
                'date_debut': datetime.date(2025, 12, 1),
                'date_fin': datetime.date(2026, 1, 31),
                'description': "Internat rotatoire : chirurgie générale et traumatologie.",
                'lieu': "CHU Point G",
            },
            {
                'titre': "Stage Pédiatrie - Gabriel Touré",
                'date_debut': datetime.date(2026, 2, 1),
                'date_fin': datetime.date(2026, 2, 28),
                'description': "Soins pédiatriques et néonatologie.",
                'lieu': "CHU Gabriel Touré",
            },
            {
                'titre': "Stage Gynécologie-obstétrique - Point G",
                'date_debut': datetime.date(2026, 3, 1),
                'date_fin': datetime.date(2026, 3, 31),
                'description': "Suivi de grossesse, accouchements et urgences obstétricales.",
                'lieu': "CHU Point G",
            },
            {
                'titre': "Stage Pédiatrie communautaire - Gabriel Touré",
                'date_debut': datetime.date(2026, 4, 1),
                'date_fin': datetime.date(2026, 4, 30),
                'description': "Pédiatrie avancée et suivi communautaire.",
                'lieu': "CHU Gabriel Touré",
            },
            {
                'titre': "Stage Psychiatrie - Point G",
                'date_debut': datetime.date(2026, 5, 1),
                'date_fin': datetime.date(2026, 5, 31),
                'description': "Psychiatrie clinique et urgences psychiatriques.",
                'lieu': "Service de psychiatrie Point G",
            },
            {
                'titre': "Stage Urgences et soins critiques - Point G",
                'date_debut': datetime.date(2026, 6, 1),
                'date_fin': datetime.date(2026, 7, 31),
                'description': "Soins intensifs, urgences médicales et traumatologie.",
                'lieu': "CHU Point G",
            },
            {
                'titre': "Stage Soins aux personnes âgées - UGA-G",
                'date_debut': datetime.date(2026, 8, 1),
                'date_fin': datetime.date(2026, 8, 31),
                'description': "Gériatrie, soins de longue durée et prise en charge globale.",
                'lieu': "Unité de gériatrie UGA-G",
            },
            {
                'titre': "Congé / préparation année 2",
                'date_debut': datetime.date(2026, 9, 1),
                'date_fin': datetime.date(2026, 9, 30),
                'description': "Période de congé et de préparation à l'immersion en CSCOM.",
                'lieu': "FMOS MFMC",
                'actif': False,
            },
        ],
        'DES-A2': [
            {
                'titre': "Immersion CSCOM-U urbain",
                'date_debut': datetime.date(2026, 10, 1),
                'date_fin': datetime.date(2027, 3, 31),
                'description': "Stage de médecine familiale en CSCOM urbain avec supervision renforcée.",
                'lieu': "CSCOM-U urbain (Banconi)",
            },
            {
                'titre': "Immersion CSCOM-U rural",
                'date_debut': datetime.date(2027, 4, 1),
                'date_fin': datetime.date(2027, 9, 30),
                'description': "Stage de médecine communautaire en zone rurale.",
                'lieu': "CSCOM-U rural (Ségué)",
            },
        ],
        'DES-A3': [
            {
                'titre': "Consolidation clinique en CSCOM-U",
                'date_debut': datetime.date(2027, 10, 1),
                'date_fin': datetime.date(2028, 3, 31),
                'description': "Prise en charge des pathologies chroniques et coordination des soins.",
                'lieu': "CSCOM-U (urbain/rural alternés)",
            },
            {
                'titre': "Coordination et recherche-action",
                'date_debut': datetime.date(2028, 4, 1),
                'date_fin': datetime.date(2028, 9, 30),
                'description': "Leadership communautaire, audit clinique et projets de recherche-action.",
                'lieu': "CSCOM-U & CSREF partenaires",
            },
        ],
        'DES-A4': [
            {
                'titre': "Stage expertise clinique - CSCOM non universitaire",
                'date_debut': datetime.date(2028, 10, 1),
                'date_fin': datetime.date(2029, 3, 31),
                'description': "Autonomie supervisée dans un CSCOM de référence, gestion stratégique des activités.",
                'lieu': "CSCOM non universitaire rural",
            },
            {
                'titre': "Stage autonomie & mémoire",
                'date_debut': datetime.date(2029, 4, 1),
                'date_fin': datetime.date(2029, 9, 30),
                'description': "Préparation du mémoire, transfert de compétences et projet professionnel final.",
                'lieu': "FMOS / CSCOM d'affectation",
            },
        ],
    }

    for classe_code, stages in stage_data.items():
        classe = Classe.objects.filter(formation=formation, code=classe_code).first()
        if not classe:
            continue

        for stage in stages:
            titre = stage['titre']
            debut = make_datetime(stage['date_debut'], 8)
            fin = make_datetime(stage['date_fin'], 17)
            heures = ((stage['date_fin'] - stage['date_debut']).days + 1) * 8
            defaults = {
                'description': stage['description'],
                'type_activite': 'stage',
                'date_fin': fin,
                'duree_heures': min(heures, 999),
                'lieu': stage['lieu'],
                'cours_lie': None,
                'actif': stage.get('actif', True),
            }

            planification, _ = Planification.objects.get_or_create(
                classe=classe,
                titre=titre,
                date_debut=debut,
                defaults=defaults,
            )

            for field, value in defaults.items():
                setattr(planification, field, value)
            planification.save()


def unseed_planifications(apps, schema_editor):
    Formation = apps.get_model('utilisateurs', 'Formation')
    Planification = apps.get_model('utilisateurs', 'Planification')

    formation = Formation.objects.filter(code='DESMFMC').first()
    if not formation:
        return

    Planification.objects.filter(classe__formation=formation).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0006_seed_desmfmc_programme'),
    ]

    operations = [
        migrations.RunPython(seed_planifications, unseed_planifications),
    ]


