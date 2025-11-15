"""
Commande Django pour créer les signatures des membres de la coordination DESMFMC
"""
from django.core.management.base import BaseCommand
from apps.utilisateurs.models_documents import SignatureCoordination


class Command(BaseCommand):
    help = 'Crée les signatures des membres de la coordination DESMFMC'

    def handle(self, *args, **options):
        membres_coordination = [
            {
                'nom': 'TRAORE',
                'prenom': 'Fatoumata',
                'titre': 'Directeur du Programme DESMFMC',
                'est_directeur': True,
            },
            {
                'nom': 'GOÏTA',
                'prenom': 'Issa Souleymane',
                'titre': 'Adjoint au Directeur du Programme DESMFMC',
                'est_directeur': False,
            },
            {
                'nom': 'SIDIBE',
                'prenom': 'Drissa Mansa',
                'titre': 'Adjoint au Directeur du Programme DESMFMC',
                'est_directeur': False,
            },
            {
                'nom': 'SIDIBE',
                'prenom': 'Souleymane',
                'titre': 'Adjoint au Directeur du Programme DESMFMC',
                'est_directeur': False,
            },
        ]

        created_count = 0
        updated_count = 0

        for membre in membres_coordination:
            signature, created = SignatureCoordination.objects.get_or_create(
                nom_signataire=membre['nom'],
                prenom_signataire=membre['prenom'],
                defaults={
                    'titre_signataire': membre['titre'],
                    'est_directeur': membre['est_directeur'],
                    'actif': membre['est_directeur'],  # Le directeur est actif par défaut
                }
            )

            if not created:
                # Mettre à jour si elle existe déjà
                signature.titre_signataire = membre['titre']
                signature.est_directeur = membre['est_directeur']
                if membre['est_directeur']:
                    signature.actif = True
                signature.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'✓ Signature mise à jour: {signature.get_nom_complet()} - {signature.titre_signataire}')
                )
            else:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Signature créée: {signature.get_nom_complet()} - {signature.titre_signataire}')
                )

        # S'assurer qu'il n'y a qu'un seul directeur actif
        directeurs = SignatureCoordination.objects.filter(est_directeur=True)
        if directeurs.count() > 1:
            # Garder le premier et désactiver les autres
            premier_directeur = directeurs.first()
            directeurs.exclude(pk=premier_directeur.pk).update(est_directeur=False)
            self.stdout.write(
                self.style.WARNING('⚠ Plusieurs directeurs détectés. Seul le premier a été conservé comme directeur.')
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Terminé ! {created_count} signature(s) créée(s), {updated_count} signature(s) mise(s) à jour.'
            )
        )

