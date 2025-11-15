# Generated manually

from django.db import migrations
from datetime import date


def create_classes_and_assign_students(apps, schema_editor):
    """Crée les 4 classes DESMFMC et attribue les étudiants à leur classe selon leur année"""
    Formation = apps.get_model('utilisateurs', 'Formation')
    Classe = apps.get_model('utilisateurs', 'Classe')
    Utilisateur = apps.get_model('utilisateurs', 'Utilisateur')
    ResultatAnneeDES = apps.get_model('utilisateurs', 'ResultatAnneeDES')
    
    # Récupérer ou créer la formation DESMFMC
    formation, _ = Formation.objects.get_or_create(
        code='DESMFMC',
        defaults={
            'nom': "Diplôme d'Études Spécialisées en Médecine de Famille et Médecine Communautaire",
            'type_formation': 'continue',
            'nature': 'certifiante',
            'duree_annees': 4,
            'actif': True,
        }
    )
    
    # Calculer les dates pour l'année scolaire actuelle
    annee_actuelle = date.today().year
    mois_actuel = date.today().month
    
    # L'année scolaire commence en octobre
    if mois_actuel >= 10:
        annee_scolaire_debut = annee_actuelle
        annee_scolaire_fin = annee_actuelle + 1
    else:
        annee_scolaire_debut = annee_actuelle - 1
        annee_scolaire_fin = annee_actuelle
    
    # Créer ou mettre à jour les 4 classes
    classes_data = [
        {
            'code': 'DES-A1',
            'nom': "DESMFMC - Année 1 Internat rotatoire",
            'annee': 1,
            'date_debut': date(annee_scolaire_debut, 10, 1),
            'date_fin': date(annee_scolaire_fin, 9, 30),
            'description': """Six mois d'internat rotatoire hospitalier (médecine interne, chirurgie générale, pédiatrie,
                gynéco-obstétrique, psychiatrie, urgences, soins aux personnes âgées) complétés par 144 heures
                d'enseignements théoriques ciblés sur la première ligne.""",
            'effectif_max': 50,
        },
        {
            'code': 'DES-A2',
            'nom': "DESMFMC - Année 2 Immersion CSCOM-U",
            'annee': 2,
            'date_debut': date(annee_scolaire_debut, 10, 1),
            'date_fin': date(annee_scolaire_fin, 9, 30),
            'description': """Année complète en CSCOM universitaire (urbain ou rural) dédiée à l'acquisition des compétences
                communautaires, de gestion de programmes et de coordination des ressources de première ligne.""",
            'effectif_max': 50,
        },
        {
            'code': 'DES-A3',
            'nom': "DESMFMC - Année 3 Consolidation communautaire",
            'annee': 3,
            'date_debut': date(annee_scolaire_debut, 10, 1),
            'date_fin': date(annee_scolaire_fin, 9, 30),
            'description': """Deuxième année d'immersion CSCOM-U alternant milieu urbain et rural, avec renforcement des
                compétences en maladies chroniques, promotion de la santé, recherche-action et coordination.""",
            'effectif_max': 50,
        },
        {
            'code': 'DES-A4',
            'nom': "DESMFMC - Année 4 Autonomie et expertise",
            'annee': 4,
            'date_debut': date(annee_scolaire_debut, 10, 1),
            'date_fin': date(annee_scolaire_fin, 9, 30),
            'description': """Stages avancés en autonomie dans un CSCOM non universitaire complétés par des modules
                d'expertise clinique, de gestion stratégique, de supervision d'équipes et de préparation du mémoire.""",
            'effectif_max': 50,
        },
    ]
    
    classes_map = {}
    for data in classes_data:
        classe, created = Classe.objects.get_or_create(
            formation=formation,
            code=data['code'],
            defaults={
                'nom': data['nom'],
                'annee': data['annee'],
                'date_debut': data['date_debut'],
                'date_fin': data['date_fin'],
                'description': data['description'],
                'effectif_max': data['effectif_max'],
                'actif': True,
            },
        )
        # Mettre à jour même si la classe existe déjà
        classe.nom = data['nom']
        classe.annee = data['annee']
        classe.date_debut = data['date_debut']
        classe.date_fin = data['date_fin']
        classe.description = data['description']
        classe.effectif_max = data['effectif_max']
        classe.actif = True
        classe.save()
        classes_map[data['annee']] = classe
    
    # Attribuer les étudiants à leur classe selon leur année
    # On traite uniquement les étudiants qui sont déjà dans le DESMFMC ou qui n'ont pas encore de classe
    etudiants = Utilisateur.objects.filter(
        type_utilisateur='etudiant',
        is_active=True
    )
    
    for etudiant in etudiants:
        # Vérifier si l'étudiant est déjà dans le DESMFMC ou s'il n'a pas de classe
        est_desmfmc = False
        if etudiant.classe:
            # Vérifier si la classe actuelle contient DESMFMC
            est_desmfmc = 'DESMFMC' in etudiant.classe or 'DES-A' in etudiant.classe
        else:
            # Si pas de classe, vérifier s'il a des résultats DESMFMC
            est_desmfmc = ResultatAnneeDES.objects.filter(
                etudiant=etudiant,
                formation=formation
            ).exists()
        
        # Ne traiter que les étudiants du DESMFMC ou ceux sans classe
        if not est_desmfmc and etudiant.classe:
            continue
        
        annee_etudiant = None
        
        # Déterminer l'année de l'étudiant basée sur ses résultats
        try:
            # Chercher le résultat le plus récent
            resultats = ResultatAnneeDES.objects.filter(
                etudiant=etudiant,
                formation=formation
            ).order_by('-annee')
            
            if resultats.exists():
                dernier_resultat = resultats.first()
                
                # Si l'étudiant a été admis en année N, il est maintenant en année N+1
                if dernier_resultat.decision == 'admis':
                    annee_etudiant = dernier_resultat.annee + 1
                # Si l'étudiant est diplômé, il reste en année 4
                elif dernier_resultat.decision == 'diplome':
                    annee_etudiant = 4
                # Si l'étudiant est en cours d'évaluation ou ajourné, il reste dans la même année
                else:
                    annee_etudiant = dernier_resultat.annee
            else:
                # Si l'étudiant n'a pas de résultat mais a une classe DESMFMC, essayer de déterminer depuis la classe
                if etudiant.classe and ('Année 1' in etudiant.classe or 'DES-A1' in etudiant.classe):
                    annee_etudiant = 1
                elif etudiant.classe and ('Année 2' in etudiant.classe or 'DES-A2' in etudiant.classe):
                    annee_etudiant = 2
                elif etudiant.classe and ('Année 3' in etudiant.classe or 'DES-A3' in etudiant.classe):
                    annee_etudiant = 3
                elif etudiant.classe and ('Année 4' in etudiant.classe or 'DES-A4' in etudiant.classe):
                    annee_etudiant = 4
                else:
                    # Par défaut, année 1 pour les nouveaux étudiants
                    annee_etudiant = 1
        except Exception:
            # En cas d'erreur, mettre en année 1 par défaut
            annee_etudiant = 1
        
        # Limiter l'année entre 1 et 4
        annee_etudiant = max(1, min(4, annee_etudiant))
        
        # Attribuer la classe correspondante
        if annee_etudiant in classes_map:
            classe_attribuee = classes_map[annee_etudiant]
            etudiant.classe = classe_attribuee.nom
            etudiant.save()


def reverse_create_classes_and_assign_students(apps, schema_editor):
    """Annule les attributions de classes (ne supprime pas les classes)"""
    Utilisateur = apps.get_model('utilisateurs', 'Utilisateur')
    
    # Réinitialiser les classes des étudiants DESMFMC
    etudiants = Utilisateur.objects.filter(
        type_utilisateur='etudiant',
        classe__icontains='DESMFMC'
    )
    
    for etudiant in etudiants:
        etudiant.classe = ''
        etudiant.save()


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0032_update_cscom_superviseurs'),
    ]

    operations = [
        migrations.RunPython(create_classes_and_assign_students, reverse_create_classes_and_assign_students),
    ]

