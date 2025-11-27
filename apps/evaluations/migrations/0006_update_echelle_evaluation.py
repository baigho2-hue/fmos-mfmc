# Generated manually to update evaluation scales
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluations', '0005_critereevaluation_elementevaluation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grilleevaluation',
            name='echelle_evaluation',
            field=models.CharField(
                choices=[
                    ('1-5', '1 : Insuffisante · 2 : Inconstante/Inférieure aux attentes · 3 : Conforme aux attentes · 4 : Dépasse nettement les attentes · 5 : NA (Non Applicable)'),
                    ('0-20', 'Note sur 20'),
                    ('0-100', 'Pourcentage (0-100)'),
                ],
                default='1-5',
                max_length=20,
                verbose_name="Échelle d'évaluation"
            ),
        ),
        migrations.AlterField(
            model_name='reponsecritere',
            name='niveau',
            field=models.CharField(
                blank=True,
                choices=[
                    ('1', '1 : Insuffisante'),
                    ('2', '2 : Inconstante/Inférieure aux attentes'),
                    ('3', '3 : Conforme aux attentes'),
                    ('4', '4 : Dépasse nettement les attentes'),
                    ('5', '5 : NA (Non Applicable)'),
                ],
                max_length=20,
                null=True,
                verbose_name='Niveau atteint'
            ),
        ),
        migrations.AlterField(
            model_name='reponseelement',
            name='niveau',
            field=models.CharField(
                blank=True,
                choices=[
                    ('1', '1 : Insuffisante'),
                    ('2', '2 : Inconstante/Inférieure aux attentes'),
                    ('3', '3 : Conforme aux attentes'),
                    ('4', '4 : Dépasse nettement les attentes'),
                    ('5', '5 : NA (Non Applicable)'),
                ],
                max_length=20,
                null=True,
                verbose_name='Niveau atteint'
            ),
        ),
    ]

