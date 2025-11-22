# Generated migration - Rename PaiementCours to PaiementFormation
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import django.core.validators


def migrate_cours_to_formation(apps, schema_editor):
    """Migre les données de cours vers formation"""
    PaiementCours = apps.get_model('utilisateurs', 'PaiementCours')
    PaiementFormation = apps.get_model('utilisateurs', 'PaiementFormation')
    Formation = apps.get_model('utilisateurs', 'Formation')
    Classe = apps.get_model('utilisateurs', 'Classe')
    
    # Pour chaque paiement, trouver la formation correspondante via la classe du cours
    for paiement_cours in PaiementCours.objects.all():
        if paiement_cours.cours and paiement_cours.cours.classe:
            classe = paiement_cours.cours.classe
            formation = classe.formation
            
            # Créer le nouveau paiement formation
            PaiementFormation.objects.create(
                id=paiement_cours.id,
                formation=formation,
                etudiant=paiement_cours.etudiant,
                montant=paiement_cours.montant,
                mode_paiement=paiement_cours.mode_paiement,
                statut=paiement_cours.statut,
                reference_paiement=paiement_cours.reference_paiement,
                preuve_paiement=paiement_cours.preuve_paiement,
                date_paiement=paiement_cours.date_paiement,
                date_validation=paiement_cours.date_validation,
                valideur=paiement_cours.valideur,
                commentaires=paiement_cours.commentaires,
                date_creation=paiement_cours.date_creation,
                date_modification=paiement_cours.date_modification,
            )


def reverse_migrate(apps, schema_editor):
    """Migration inverse"""
    PaiementCours = apps.get_model('utilisateurs', 'PaiementCours')
    PaiementFormation = apps.get_model('utilisateurs', 'PaiementFormation')
    Cours = apps.get_model('utilisateurs', 'Cours')
    
    # Pour chaque paiement formation, trouver un cours de la formation
    for paiement_formation in PaiementFormation.objects.all():
        if paiement_formation.formation:
            # Prendre le premier cours de la première classe de la formation
            classes = paiement_formation.formation.classes.all()
            if classes.exists():
                classe = classes.first()
                cours = classe.cours.first()
                if cours:
                    PaiementCours.objects.create(
                        id=paiement_formation.id,
                        cours=cours,
                        etudiant=paiement_formation.etudiant,
                        montant=paiement_formation.montant,
                        mode_paiement=paiement_formation.mode_paiement,
                        statut=paiement_formation.statut,
                        reference_paiement=paiement_formation.reference_paiement,
                        preuve_paiement=paiement_formation.preuve_paiement,
                        date_paiement=paiement_formation.date_paiement,
                        date_validation=paiement_formation.date_validation,
                        valideur=paiement_formation.valideur,
                        commentaires=paiement_formation.commentaires,
                        date_creation=paiement_formation.date_creation,
                        date_modification=paiement_formation.date_modification,
                    )


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0035_coutformation_bourse_offerte'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Créer le nouveau modèle PaiementFormation
        migrations.CreateModel(
            name='PaiementFormation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant')),
                ('mode_paiement', models.CharField(choices=[('bancaire', 'Bancaire'), ('espece', 'Espèce'), ('orange_money', 'Orange Money')], default='bancaire', max_length=20, verbose_name='Mode de paiement')),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('valide', 'Validé'), ('refuse', 'Refusé')], default='en_attente', max_length=20, verbose_name='Statut')),
                ('reference_paiement', models.CharField(blank=True, help_text='Référence du paiement (numéro de transaction, etc.)', max_length=100, null=True, verbose_name='Référence de paiement')),
                ('preuve_paiement', models.FileField(blank=True, help_text="Capture d'écran, reçu, etc.", null=True, upload_to='formations/preuves_paiement/', verbose_name='Preuve de paiement')),
                ('date_paiement', models.DateTimeField(auto_now_add=True, verbose_name='Date de paiement')),
                ('date_validation', models.DateTimeField(blank=True, null=True, verbose_name='Date de validation')),
                ('commentaires', models.TextField(blank=True, null=True, verbose_name='Commentaires')),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('etudiant', models.ForeignKey(limit_choices_to={'type_utilisateur': 'etudiant'}, on_delete=django.db.models.deletion.CASCADE, related_name='paiements_formations', to=settings.AUTH_USER_MODEL, verbose_name='Étudiant')),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paiements', to='utilisateurs.formation', verbose_name='Formation')),
                ('valideur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paiements_formations_valides', to=settings.AUTH_USER_MODEL, verbose_name='Validateur')),
            ],
            options={
                'verbose_name': 'Paiement de formation',
                'verbose_name_plural': 'Paiements de formations',
                'ordering': ['-date_paiement'],
                'unique_together': {('formation', 'etudiant')},
            },
        ),
        # Migrer les données
        migrations.RunPython(migrate_cours_to_formation, reverse_migrate),
        # Supprimer l'ancien modèle
        migrations.DeleteModel(
            name='PaiementCours',
        ),
    ]
