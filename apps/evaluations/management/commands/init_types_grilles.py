"""
Commande pour initialiser les types de grilles d'évaluation
"""
from django.core.management.base import BaseCommand
from apps.evaluations.models_grilles import TypeGrilleEvaluation


class Command(BaseCommand):
    help = "Initialise les types de grilles d'évaluation"

    def handle(self, *args, **options):
        types_grilles = [
            {
                'code': 'FORMATIVE',
                'nom': 'Évaluation Formative',
                'description': 'Évaluation continue permettant de suivre les progrès et d\'identifier les besoins d\'apprentissage',
                'type_grille': 'formative',
            },
            {
                'code': 'SOMMATIVE',
                'nom': 'Évaluation Sommative',
                'description': 'Évaluation à la fin d\'une période d\'apprentissage pour mesurer les acquis',
                'type_grille': 'sommative',
            },
            {
                'code': 'FINALE',
                'nom': 'Évaluation Finale',
                'description': 'Évaluation finale du programme ou de la formation',
                'type_grille': 'finale',
            },
            {
                'code': 'SUPERVISION',
                'nom': 'Grille de Supervision',
                'description': 'Grille pour l\'évaluation lors des supervisions cliniques',
                'type_grille': 'supervision',
            },
            {
                'code': 'SIMULATION',
                'nom': 'Activité de Simulation',
                'description': 'Grille pour évaluer les activités de simulation clinique',
                'type_grille': 'simulation',
            },
            {
                'code': 'SCENARIO',
                'nom': 'Activité de Scénario',
                'description': 'Grille pour évaluer les activités basées sur des scénarios cliniques',
                'type_grille': 'scenario',
            },
            {
                'code': 'PRESENTATION',
                'nom': 'Présentation',
                'description': 'Grille pour évaluer les présentations orales et les exposés',
                'type_grille': 'presentation',
            },
            {
                'code': 'HABILETES_CLINIQUES',
                'nom': 'Habiletés Cliniques',
                'description': 'Grille pour évaluer les habiletés et compétences cliniques pratiques',
                'type_grille': 'habiletes_cliniques',
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

