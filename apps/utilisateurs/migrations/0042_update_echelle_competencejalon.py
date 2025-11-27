# Generated manually to update evaluation scale for CompetenceJalon
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0040_competencejalon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competencejalon',
            name='echelle_evaluation',
            field=models.CharField(
                choices=[
                    ('1-5', '1 : Insuffisante · 2 : Inconstante/Inférieure aux attentes · 3 : Conforme aux attentes · 4 : Dépasse nettement les attentes · 5 : NA (Non Applicable)'),
                ],
                default='1-5',
                max_length=20,
                verbose_name="Échelle d'évaluation"
            ),
        ),
    ]

