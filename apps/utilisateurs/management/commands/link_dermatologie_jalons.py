"""
Commande pour lier les cours de dermatologie aux jalons de la compétence Expert médical
pour les années 2 et 3.
"""
from django.core.management.base import BaseCommand
from apps.utilisateurs.models_formation import (
    Formation,
    Classe,
    Cours,
    Competence,
    CompetenceJalon,
)


class Command(BaseCommand):
    help = "Lie les cours de dermatologie aux jalons de la compétence Expert médical (années 2 et 3)"

    def handle(self, *args, **options):
        try:
            formation = Formation.objects.get(code='DESMFMC')
        except Formation.DoesNotExist:
            self.stdout.write(self.style.ERROR("Formation DESMFMC introuvable."))
            return

        # Récupérer la compétence Expert médical
        try:
            competence = Competence.objects.get(libelle="Expert médical en MF/MC")
        except Competence.DoesNotExist:
            self.stdout.write(self.style.ERROR("Compétence 'Expert médical en MF/MC' introuvable."))
            return

        # Traiter les années 2 et 3
        for annee in [2, 3]:
            classe_code = f"DES-A{annee}"
            try:
                classe = Classe.objects.get(code=classe_code, formation=formation)
            except Classe.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Classe {classe_code} introuvable, passage à l'année suivante."))
                continue

            # Récupérer tous les jalons Expert médical pour cette classe
            jalons = CompetenceJalon.objects.filter(
                competence=competence,
                classe=classe
            )

            if not jalons.exists():
                self.stdout.write(self.style.WARNING(f"Aucun jalon Expert médical trouvé pour {classe_code}."))
                continue

            # Récupérer les cours de dermatologie pour cette classe
            cours_derm = Cours.objects.filter(
                classe=classe,
                code__in=[f"DES-A{annee}-DERM"]
            )

            if not cours_derm.exists():
                self.stdout.write(self.style.WARNING(f"Aucun cours de dermatologie trouvé pour {classe_code}."))
                continue

            # Lier chaque cours de dermatologie à tous les jalons Expert médical de cette classe
            for cours in cours_derm:
                for jalon in jalons:
                    if jalon not in cours.jalons_competence.all():
                        cours.jalons_competence.add(jalon)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"✓ Cours '{cours.titre}' lié au jalon '{jalon.titre}' ({classe_code})"
                            )
                        )
                    else:
                        self.stdout.write(
                            f"  Cours '{cours.titre}' déjà lié au jalon '{jalon.titre}' ({classe_code})"
                        )

        self.stdout.write(self.style.SUCCESS("\n✅ Liaison des cours de dermatologie terminée."))

