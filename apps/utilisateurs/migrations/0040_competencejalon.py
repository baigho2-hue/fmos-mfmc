from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0039_add_competences_jalons_classes'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetenceJalon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=300, verbose_name='Titre du jalon')),
                ('description', models.TextField(verbose_name='Description / critères observables')),
                ('echelle_evaluation', models.CharField(choices=[('1-4', '1 : Insuffisant · 2 : Inconstant · 3 : Conforme · 4 : Dépasse les attentes'), ('1-5', '1 : Insuffisant · 2 : Inconstant · 3 : Conforme · 4 : Dépasse · 5 : N/A')], default='1-5', max_length=20, verbose_name="Échelle d'évaluation")),
                ('ordre', models.IntegerField(default=0, verbose_name="Ordre d'affichage")),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('classe', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='jalons_competence', to='utilisateurs.classe', verbose_name='Classe concernée')),
                ('competence', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='jalons_competence', to='utilisateurs.competence', verbose_name='Compétence associée')),
            ],
            options={
                'verbose_name': 'Jalon de compétence',
                'verbose_name_plural': 'Jalons de compétences',
                'ordering': ['classe__annee', 'competence__libelle', 'ordre', 'titre'],
                'unique_together': {('competence', 'classe', 'titre')},
            },
        ),
        migrations.AddField(
            model_name='cours',
            name='jalons_competence',
            field=models.ManyToManyField(blank=True, related_name='cours', to='utilisateurs.competencejalon', verbose_name='Jalons évalués'),
        ),
    ]

