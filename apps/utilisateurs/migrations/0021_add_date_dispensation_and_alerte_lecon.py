# Generated manually
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0020_listemed6_alter_etudiantmed6_matricule_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecon',
            name='date_dispensation',
            field=models.DateTimeField(blank=True, help_text='Date et heure prévues pour dispenser cette leçon', null=True, verbose_name='Date et heure de dispensation'),
        ),
        migrations.CreateModel(
            name='AlerteLecon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_alerte', models.CharField(choices=[('semaine', '1 semaine avant'), ('trois_jours', '3 jours avant'), ('programmee', 'Lors de la programmation')], max_length=20, verbose_name="Type d'alerte")),
                ('date_envoi', models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")),
                ('envoye', models.BooleanField(default=True, verbose_name='Envoyé')),
                ('enseignant', models.ForeignKey(limit_choices_to={'type_utilisateur': 'enseignant'}, on_delete=django.db.models.deletion.CASCADE, related_name='alertes_lecons', to='utilisateurs.utilisateur', verbose_name='Enseignant')),
                ('lecon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alertes', to='utilisateurs.lecon', verbose_name='Leçon')),
            ],
            options={
                'verbose_name': 'Alerte de leçon',
                'verbose_name_plural': 'Alertes de leçons',
                'ordering': ['-date_envoi'],
                'unique_together': {('lecon', 'enseignant', 'type_alerte')},
            },
        ),
    ]

