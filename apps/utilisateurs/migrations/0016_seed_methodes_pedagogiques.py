"""
Migration pour insérer les méthodes pédagogiques
"""
from django.db import migrations


def seed_methodes_pedagogiques(apps, schema_editor):
    """Insère les méthodes pédagogiques dans la base de données"""
    MethodePedagogique = apps.get_model('utilisateurs', 'MethodePedagogique')
    
    methodes = [
        {
            'nom': 'Méthode Magistrale',
            'description': 'Cours magistral où l\'enseignant transmet les connaissances de manière unidirectionnelle aux étudiants.',
            'avantages': 'Permet de couvrir beaucoup de contenu en peu de temps, efficace pour les grandes classes.',
            'inconvenients': 'Peut être passif pour les étudiants, nécessite une bonne attention.',
            'contexte_utilisation': 'Cours théoriques, introduction de nouveaux concepts, grandes classes.'
        },
        {
            'nom': 'Jeu de rôle',
            'description': 'Technique où les étudiants jouent des rôles spécifiques pour explorer des situations réelles.',
            'avantages': 'Développe l\'empathie, la communication, permet de pratiquer dans un environnement sécurisé.',
            'inconvenients': 'Peut être intimidant pour certains étudiants, nécessite une bonne préparation.',
            'contexte_utilisation': 'Formation à la communication, gestion de situations difficiles, pratique clinique.'
        },
        {
            'nom': 'Simulation',
            'description': 'Reproduction d\'une situation réelle dans un environnement contrôlé pour la pratique.',
            'avantages': 'Permet de pratiquer sans risque, répétition possible, feedback immédiat.',
            'inconvenients': 'Peut être coûteux, nécessite du matériel spécialisé.',
            'contexte_utilisation': 'Simulation médicale, gestes techniques, urgences, procédures cliniques.'
        },
        {
            'nom': 'Démonstration',
            'description': 'L\'enseignant montre une technique ou une procédure que les étudiants observent puis reproduisent.',
            'avantages': 'Visuel et concret, permet de voir la bonne façon de faire, facilite l\'apprentissage pratique.',
            'inconvenients': 'Peut nécessiter du matériel, limité par le nombre d\'observateurs.',
            'contexte_utilisation': 'Techniques médicales, gestes pratiques, procédures cliniques, utilisation d\'équipements.'
        },
        {
            'nom': 'Études de cas',
            'description': 'Analyse de situations réelles ou fictives pour appliquer les connaissances théoriques.',
            'avantages': 'Lien théorie-pratique, développement du raisonnement clinique, apprentissage actif.',
            'inconvenients': 'Peut être complexe, nécessite une bonne préparation des cas.',
            'contexte_utilisation': 'Diagnostic différentiel, prise de décision clinique, analyse de situations complexes.'
        },
        {
            'nom': 'Travaux pratiques',
            'description': 'Sessions où les étudiants pratiquent activement des techniques ou manipulations sous supervision.',
            'avantages': 'Apprentissage pratique, développement de compétences techniques, application directe.',
            'inconvenients': 'Nécessite supervision, matériel et espace, limité par le ratio encadrant/étudiants.',
            'contexte_utilisation': 'Techniques de soins, manipulations, examens cliniques, procédures pratiques.'
        },
    ]
    
    for methode_data in methodes:
        MethodePedagogique.objects.get_or_create(
            nom=methode_data['nom'],
            defaults=methode_data
        )
    
    print(f"[OK] {len(methodes)} methodes pedagogiques inserees")


def unseed_methodes_pedagogiques(apps, schema_editor):
    """Supprime les méthodes pédagogiques créées"""
    MethodePedagogique = apps.get_model('utilisateurs', 'MethodePedagogique')
    
    noms_a_supprimer = [
        'Méthode Magistrale',
        'Jeu de rôle',
        'Simulation',
        'Démonstration',
        'Études de cas',
        'Travaux pratiques',
    ]
    
    MethodePedagogique.objects.filter(nom__in=noms_a_supprimer).delete()
    print("[OK] Methodes pedagogiques supprimees")


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0015_questionquiz_quizlecon_reponsequestion_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_methodes_pedagogiques, unseed_methodes_pedagogiques),
    ]

