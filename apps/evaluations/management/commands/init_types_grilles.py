"""
Commande pour initialiser les types de grilles d'évaluation
"""
from django.core.management.base import BaseCommand
from apps.evaluations.models_grilles import TypeGrilleEvaluation


class Command(BaseCommand):
    help = "Initialise les types de grilles d'évaluation"

    def handle(self, *args, **options):
        types_grilles = [
            # Grilles d'apprentissage
            {
                'code': 'HABILETES_CLINIQUES',
                'nom': 'Habilités Cliniques',
                'description': 'Grille d\'apprentissage pour évaluer les habiletés et compétences cliniques pratiques',
                'type_grille': 'habiletes_cliniques',
            },
            {
                'code': 'FORMATIVE',
                'nom': 'Évaluation Formative',
                'description': 'Grille d\'apprentissage - Évaluation continue permettant de suivre les progrès et d\'identifier les besoins d\'apprentissage',
                'type_grille': 'formative',
            },
            {
                'code': 'SCENARIO',
                'nom': 'Scénario',
                'description': 'Grille d\'apprentissage pour évaluer les activités basées sur des scénarios cliniques',
                'type_grille': 'scenario',
            },
            # Grilles d'évaluation finale/sommative
            {
                'code': 'SOMMATIVE',
                'nom': 'Évaluation Sommative',
                'description': 'Grille d\'évaluation sommative - Évaluation à la fin d\'une période d\'apprentissage pour mesurer les acquis',
                'type_grille': 'sommative',
            },
            {
                'code': 'FINALE',
                'nom': 'Évaluation Finale',
                'description': 'Grille d\'évaluation finale - Évaluation finale du programme ou de la formation',
                'type_grille': 'finale',
            },
            # Grilles de supervision
            {
                'code': 'SUPERVISION_DIRECTE_INDIRECTE',
                'nom': 'Supervision Directe ou Indirecte',
                'description': 'Grille pour l\'évaluation lors des supervisions cliniques directes ou indirectes',
                'type_grille': 'supervision_directe_indirecte',
            },
            {
                'code': 'METASUPERVISION',
                'nom': 'Métasupervision',
                'description': 'Grille pour l\'évaluation lors des métasupervisions (supervision de la supervision)',
                'type_grille': 'metasupervision',
            },
            # Autres types
            {
                'code': 'SIMULATION',
                'nom': 'Activité de Simulation',
                'description': 'Grille pour évaluer les activités de simulation clinique',
                'type_grille': 'simulation',
            },
            {
                'code': 'PRESENTATION',
                'nom': 'Présentation',
                'description': 'Grille pour évaluer les présentations orales et les exposés',
                'type_grille': 'presentation',
            },
        ]

        created_count = 0
        updated_count = 0

        for type_data in types_grilles:
            type_grille, created = TypeGrilleEvaluation.objects.update_or_create(
                code=type_data['code'],
                defaults={
                    'nom': type_data['nom'],
                    'description': type_data['description'],
                    'type_grille': type_data['type_grille'],
                    'actif': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Créé: {type_grille.nom}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Mis à jour: {type_grille.nom}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Initialisation terminée:\n'
                f'  - {created_count} types créés\n'
                f'  - {updated_count} types mis à jour\n'
            )
        )

