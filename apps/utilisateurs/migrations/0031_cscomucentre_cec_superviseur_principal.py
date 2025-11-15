# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0030_utilisateur_centre_supervision'),
    ]

    operations = [
        migrations.AddField(
            model_name='cscomucentre',
            name='cec_superviseur_principal',
            field=models.CharField(blank=True, max_length=200, verbose_name='CEC/Superviseur Principal'),
        ),
    ]

