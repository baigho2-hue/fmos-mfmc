from django.db import migrations
import datetime
import textwrap


def seed_desmfmc_programme(apps, schema_editor):
    Formation = apps.get_model('utilisateurs', 'Formation')
    Classe = apps.get_model('utilisateurs', 'Classe')
    Cours = apps.get_model('utilisateurs', 'Cours')
    Competence = apps.get_model('utilisateurs', 'Competence')
    JalonProgramme = apps.get_model('utilisateurs', 'JalonProgramme')
    ModuleProgramme = apps.get_model('utilisateurs', 'ModuleProgramme')
    CoursProgramme = apps.get_model('utilisateurs', 'CoursProgramme')

    # ------------------------------------------------------------------
    # Formation DESMFMC
    # ------------------------------------------------------------------
    formation_defaults = {
        'nom': "Diplôme d'Études Spécialisées en Médecine de Famille et Médecine Communautaire",
        'description': textwrap.dedent("""
            Programme professionnalisant de quatre années qui combine internat rotatoire hospitalier,
            immersion prolongée dans des CSCOM universitaires (urbain et rural) et stages avancés en
            autonomie. Il prépare les médecins à offrir des soins de première ligne complets, continus,
            centrés sur la communauté et intégrant gestion, prévention et leadership clinique.
        """).strip(),
        'type_formation': 'continue',
        'nature': 'certifiante',
        'duree_annees': 4,
        'duree_heures': 617,  # 144 + 165 + 175 + 133 heures théoriques
        'objectifs_generaux': textwrap.dedent("""
            1. Dispenser les soins curatifs, préventifs et promotionnels de première ligne au sein d'une population donnée.
            2. Développer une relation thérapeutique continue et personnalisée avec les patients et leur communauté.
            3. Collaborer avec l'ensemble des acteurs professionnels et communautaires du réseau de soins.
            4. Assurer le leadership en prévention, promotion de la santé et intervention communautaire.
            5. Gérer et organiser des services de santé accessibles, disponibles et de qualité.
            6. Intervenir avec professionnalisme et éthique dans tous les contextes de pratique.
            7. Maintenir et développer ses compétences par une démarche d'auto-apprentissage et d'érudition.
        """).strip(),
        'competences_visées': textwrap.dedent("""
            • Expert médical en médecine de famille/médecine communautaire.
            • Communicateur auprès des patients, des familles et des partenaires.
            • Collaborateur avec les ressources professionnelles et communautaires.
            • Promoteur de la santé et leader en prévention.
            • Gestionnaire des services de première ligne et des programmes nationaux.
            • Érudit capable d'analyse critique et de recherche-action.
            • Professionnel responsable, éthique et engagé envers la communauté.
        """).strip(),
        'prerequis': textwrap.dedent("""
            Doctorat en médecine, réussite au concours d'internat et engagement à exercer en première ligne
            dans un contexte communautaire au Mali ou en région partenaire.
        """).strip(),
        'debouches': textwrap.dedent("""
            Médecin de famille/médecin communautaire, coordonnateur de CSCOM, responsable de programmes
            de santé publique, leader de réseau de soins de premier recours ou enseignant clinicien.
        """).strip(),
    }

    formation, _ = Formation.objects.get_or_create(
        code='DESMFMC',
        defaults=formation_defaults,
    )
    # Mettre à jour systématiquement les champs clés
    for field, value in formation_defaults.items():
        setattr(formation, field, value)
    formation.actif = True
    formation.save()

    # ------------------------------------------------------------------
    # Compétences générales (7 compétences de base du DESMFMC)
    # ------------------------------------------------------------------
    competences_data = {
        'expert_medical': {
            'libelle': "Expert médical en MF/MC",
            'domaine': 'savoir_faire',
            'description': textwrap.dedent("""
                Dispenser l'ensemble des soins curatifs, préventifs et promotionnels de première
                ligne dans une aire de santé ou auprès d'une population dont il a la responsabilité.
            """).strip(),
        },
        'communicateur': {
            'libelle': "Communicateur",
            'domaine': 'savoir_etre',
            'description': textwrap.dedent("""
                Développer une relation de confiance, continue et personnalisée avec les patients et
                leur communauté, basée sur la compréhension globale de leur réalité et leurs perspectives.
            """).strip(),
        },
        'collaborateur': {
            'libelle': "Collaborateur",
            'domaine': 'savoir_etre',
            'description': textwrap.dedent("""
                Travailler en étroite collaboration avec les différentes ressources professionnelles et
                communautaires de son milieu de même qu'avec celles du réseau de soins.
            """).strip(),
        },
        'promoteur': {
            'libelle': "Promoteur de la santé",
            'domaine': 'savoir_faire',
            'description': textwrap.dedent("""
                Assumer un leadership en matière de prévention, de promotion de la santé et
                d'intervention communautaire auprès de la population qu'il dessert.
            """).strip(),
        },
        'gestionnaire': {
            'libelle': "Gestionnaire",
            'domaine': 'savoir_faire',
            'description': textwrap.dedent("""
                Gérer la planification et la mise en œuvre de services de qualité et de stratégies
                avancées efficaces en fonction des besoins de la communauté.
            """).strip(),
        },
        'professionnel': {
            'libelle': "Professionnel",
            'domaine': 'savoir_etre',
            'description': textwrap.dedent("""
                Intervenir avec professionnalisme et de manière éthique auprès des patients et des
                autres membres du réseau de soins.
            """).strip(),
        },
        'erudit': {
            'libelle': "Érudit",
            'domaine': 'savoir',
            'description': textwrap.dedent("""
                Planifier le maintien et le développement de ses compétences professionnelles en
                fonction des besoins normatifs et de sa communauté.
            """).strip(),
        },
    }

    competences_map = {}
    for key, data in competences_data.items():
        competence, _ = Competence.objects.get_or_create(
            libelle=data['libelle'],
            defaults={
                'domaine': data['domaine'],
                'description': data['description'],
                'niveau_attendu': "Maîtrise opérationnelle à l'issue du programme",
            },
        )
        # Mise à jour des champs descriptifs (idempotent)
        competence.domaine = data['domaine']
        competence.description = data['description']
        competence.niveau_attendu = "Maîtrise opérationnelle à l'issue du programme"
        competence.save()
        competences_map[key] = competence

    # ------------------------------------------------------------------
    # Classes / Cohortes
    # ------------------------------------------------------------------
    classes_data = [
        {
            'code': 'DES-A1',
            'nom': "DESMFMC - Année 1 Internat rotatoire",
            'annee': 1,
            'date_debut': datetime.date(2025, 10, 1),
            'date_fin': datetime.date(2026, 9, 30),
            'description': textwrap.dedent("""
                Six mois d'internat rotatoire hospitalier (médecine interne, chirurgie générale, pédiatrie,
                gynéco-obstétrique, psychiatrie, urgences, soins aux personnes âgées) complétés par 144 heures
                d'enseignements théoriques ciblés sur la première ligne.
            """).strip(),
            'effectif_max': 10,
        },
        {
            'code': 'DES-A2',
            'nom': "DESMFMC - Année 2 Immersion CSCOM-U",
            'annee': 2,
            'date_debut': datetime.date(2026, 10, 1),
            'date_fin': datetime.date(2027, 9, 30),
            'description': textwrap.dedent("""
                Année complète en CSCOM universitaire (urbain ou rural) dédiée à l'acquisition des compétences
                communautaires, de gestion de programmes et de coordination des ressources de première ligne.
            """).strip(),
            'effectif_max': 10,
        },
        {
            'code': 'DES-A3',
            'nom': "DESMFMC - Année 3 Consolidation communautaire",
            'annee': 3,
            'date_debut': datetime.date(2027, 10, 1),
            'date_fin': datetime.date(2028, 9, 30),
            'description': textwrap.dedent("""
                Deuxième année d'immersion CSCOM-U alternant milieu urbain et rural, avec renforcement des
                compétences en maladies chroniques, promotion de la santé, recherche-action et coordination.
            """).strip(),
            'effectif_max': 10,
        },
        {
            'code': 'DES-A4',
            'nom': "DESMFMC - Année 4 Autonomie et expertise",
            'annee': 4,
            'date_debut': datetime.date(2028, 10, 1),
            'date_fin': datetime.date(2029, 9, 30),
            'description': textwrap.dedent("""
                Stages avancés en autonomie dans un CSCOM non universitaire complétés par des modules
                d'expertise clinique, de gestion stratégique, de supervision d'équipes et de préparation du mémoire.
            """).strip(),
            'effectif_max': 10,
        },
    ]

    classes_map = {}
    for data in classes_data:
        classe, _ = Classe.objects.get_or_create(
            formation=formation,
            code=data['code'],
            defaults={
                'nom': data['nom'],
                'annee': data['annee'],
                'date_debut': data['date_debut'],
                'date_fin': data['date_fin'],
                'description': data['description'],
                'effectif_max': data['effectif_max'],
            },
        )
        classe.nom = data['nom']
        classe.annee = data['annee']
        classe.date_debut = data['date_debut']
        classe.date_fin = data['date_fin']
        classe.description = data['description']
        classe.effectif_max = data['effectif_max']
        classe.actif = True
        classe.save()
        classes_map[data['code']] = classe

    # ------------------------------------------------------------------
    # Cours théoriques (heures issues des annexes)
    # ------------------------------------------------------------------
    courses_data = [
        # Année 1
        {
            'code': 'DES-A1-C1',
            'classe_code': 'DES-A1',
            'ordre': 1,
            'titre': "Problèmes courants chez l'enfant",
            'description': "Approche clinique pédiatrique de première ligne.",
            'contenu': textwrap.dedent("""
                Diagnostic différentiel, bilans complémentaires pertinents et stratégies thérapeutiques pour les
                pathologies pédiatriques fréquentes (fièvres, infections respiratoires, troubles digestifs,
                retard staturo-pondéral, troubles du sommeil).
            """).strip(),
            'date_debut': datetime.date(2025, 10, 1),
            'date_fin': datetime.date(2025, 10, 31),
            'volume_horaire': 20,
        },
        {
            'code': 'DES-A1-C2',
            'classe_code': 'DES-A1',
            'ordre': 2,
            'titre': "Soins périnataux intégrés",
            'description': "Suivi de grossesse, accouchement et post-partum.",
            'contenu': textwrap.dedent("""
                Suivi des grossesses normales et à risque, planification familiale, techniques obstétricales,
                prévention des urgences obstétricales et promotion de l'allaitement maternel.
            """).strip(),
            'date_debut': datetime.date(2025, 11, 1),
            'date_fin': datetime.date(2025, 11, 30),
            'volume_horaire': 15,
        },
        {
            'code': 'DES-A1-C3',
            'classe_code': 'DES-A1',
            'ordre': 3,
            'titre': "Santé mentale en première ligne",
            'description': "Prise en charge des troubles anxieux, dépressifs et psychotiques.",
            'contenu': textwrap.dedent("""
                Démarche diagnostique selon le DSM, utilisation sécuritaire de la psychopharmacologie,
                indications de psychothérapie brève, repérage et gestion du risque suicidaire.
            """).strip(),
            'date_debut': datetime.date(2025, 12, 1),
            'date_fin': datetime.date(2025, 12, 31),
            'volume_horaire': 20,
        },
        {
            'code': 'DES-A1-C4',
            'classe_code': 'DES-A1',
            'ordre': 4,
            'titre': "Urgences majeures en première ligne",
            'description': "Gestion immédiate des urgences vitales.",
            'contenu': textwrap.dedent("""
                Arrêt cardio-respiratoire, choc, coma, polytraumatisme, intoxications, brûlures.
                Organisation de la salle d'urgence, triage et priorisation des interventions.
            """).strip(),
            'date_debut': datetime.date(2026, 1, 1),
            'date_fin': datetime.date(2026, 1, 31),
            'volume_horaire': 30,
        },
        {
            'code': 'DES-A1-C5',
            'classe_code': 'DES-A1',
            'ordre': 5,
            'titre': "Techniques obstétricales et habiletés chirurgicales",
            'description': "Ateliers pratiques GESTA (niveaux I et II) et FIRST.",
            'contenu': textwrap.dedent("""
                Conduite d'un accouchement eutocique, gestion des dystocies, gestes obstétricaux d'urgence,
                sutures, incisions, immobilisations et techniques chirurgicales de base.
            """).strip(),
            'date_debut': datetime.date(2026, 2, 1),
            'date_fin': datetime.date(2026, 2, 28),
            'volume_horaire': 21,
        },
        {
            'code': 'DES-A1-C6',
            'classe_code': 'DES-A1',
            'ordre': 6,
            'titre': "Soins aux adultes et aux adolescents",
            'description': "Approche globale des pathologies chroniques fréquentes.",
            'contenu': textwrap.dedent("""
                Hypertension artérielle, insuffisance cardiaque, diabète, maladies respiratoires chroniques,
                pathologies endocriniennes et suivi global de l'adolescent.
            """).strip(),
            'date_debut': datetime.date(2026, 3, 1),
            'date_fin': datetime.date(2026, 3, 31),
            'volume_horaire': 18,
        },
        {
            'code': 'DES-A1-C7',
            'classe_code': 'DES-A1',
            'ordre': 7,
            'titre': "Soins gériatriques et de fin de vie",
            'description': "Prise en charge intégrée des aînés et soins palliatifs.",
            'contenu': textwrap.dedent("""
                Évaluation gériatrique globale, pharmacologie du vieillissement, prévention des chutes,
                gestion de la douleur et accompagnement des patients en fin de vie et de leurs proches.
            """).strip(),
            'date_debut': datetime.date(2026, 4, 1),
            'date_fin': datetime.date(2026, 4, 30),
            'volume_horaire': 12,
        },
        {
            'code': 'DES-A1-C8',
            'classe_code': 'DES-A1',
            'ordre': 8,
            'titre': "Compétences transversales en MF/MC",
            'description': "Communication, collaboration et éthique clinique.",
            'contenu': textwrap.dedent("""
                Rencontre familiale, annonce de mauvaises nouvelles, gestion de cas complexes,
                documentation clinique de qualité et travail interprofessionnel.
            """).strip(),
            'date_debut': datetime.date(2026, 5, 1),
            'date_fin': datetime.date(2026, 5, 31),
            'volume_horaire': 8,
        },
        # Année 2
        {
            'code': 'DES-A2-C1',
            'classe_code': 'DES-A2',
            'ordre': 1,
            'titre': "Immersion clinique en CSCOM-U urbain",
            'description': "Organisation et parcours de soins en milieu urbain.",
            'contenu': textwrap.dedent("""
                Analyse des flux patients, stratégies de prise en charge intégrée, coordination avec les
                services de référence et adaptation des services aux besoins urbains.
            """).strip(),
            'date_debut': datetime.date(2026, 10, 1),
            'date_fin': datetime.date(2026, 12, 31),
            'volume_horaire': 40,
        },
        {
            'code': 'DES-A2-C2',
            'classe_code': 'DES-A2',
            'ordre': 2,
            'titre': "Immersion clinique en CSCOM-U rural",
            'description': "Soins de proximité et logistique en zone rurale.",
            'contenu': textwrap.dedent("""
                Organisation des tournées, supervision des relais communautaires, continuité des soins
                avec le CSREF et stratégies d'accessibilité pour les populations éloignées.
            """).strip(),
            'date_debut': datetime.date(2027, 4, 1),
            'date_fin': datetime.date(2027, 6, 30),
            'volume_horaire': 40,
        },
        {
            'code': 'DES-A2-C3',
            'classe_code': 'DES-A2',
            'ordre': 3,
            'titre': "Programmes nationaux de santé publique",
            'description': "PV, PEV, santé maternelle et infantile, maladies prioritaires.",
            'contenu': textwrap.dedent("""
                Mise en œuvre, suivi et évaluation des programmes nationaux, adaptation aux réalités locales,
                utilisation des outils SNISS et reporting auprès des autorités sanitaires.
            """).strip(),
            'date_debut': datetime.date(2026, 11, 1),
            'date_fin': datetime.date(2026, 12, 15),
            'volume_horaire': 25,
        },
        {
            'code': 'DES-A2-C4',
            'classe_code': 'DES-A2',
            'ordre': 4,
            'titre': "Communication et collaboration avancées",
            'description': "Gestion d'équipe, médiation et plaidoyer.",
            'contenu': textwrap.dedent("""
                Animation de réunions avec les autorités locales, négociation des ressources,
                accompagnement des équipes pluridisciplinaires et mobilisation communautaire.
            """).strip(),
            'date_debut': datetime.date(2027, 1, 1),
            'date_fin': datetime.date(2027, 2, 28),
            'volume_horaire': 25,
        },
        {
            'code': 'DES-A2-C5',
            'classe_code': 'DES-A2',
            'ordre': 5,
            'titre': "Urgences et obstétrique en milieu périphérique",
            'description': "Prise en charge des urgences hors plateau technique complet.",
            'contenu': textwrap.dedent("""
                Stabilisation des urgences médicales et obstétricales, transferts sécuritaires,
                protocoles d'urgence adaptés aux ressources périphériques.
            """).strip(),
            'date_debut': datetime.date(2027, 7, 1),
            'date_fin': datetime.date(2027, 7, 31),
            'volume_horaire': 20,
        },
        {
            'code': 'DES-A2-C6',
            'classe_code': 'DES-A2',
            'ordre': 6,
            'titre': "Gestion opérationnelle du CSCOM",
            'description': "Administration, finances et ressources humaines.",
            'contenu': textwrap.dedent("""
                Élaboration du plan d'action annuel, budget, gestion du personnel, supervision,
                maintenance des équipements et reporting institutionnel.
            """).strip(),
            'date_debut': datetime.date(2027, 8, 1),
            'date_fin': datetime.date(2027, 8, 31),
            'volume_horaire': 15,
        },
        # Année 3
        {
            'code': 'DES-A3-C1',
            'classe_code': 'DES-A3',
            'ordre': 1,
            'titre': "Gestion des maladies chroniques",
            'description': "Approche intégrée des pathologies chroniques en première ligne.",
            'contenu': textwrap.dedent("""
                Organisation du suivi longitudinal, clinique des maladies cardio-vasculaires, métaboliques,
                respiratoires et coordination avec les spécialistes référents.
            """).strip(),
            'date_debut': datetime.date(2027, 10, 1),
            'date_fin': datetime.date(2027, 12, 15),
            'volume_horaire': 40,
        },
        {
            'code': 'DES-A3-C2',
            'classe_code': 'DES-A3',
            'ordre': 2,
            'titre': "Santé mentale complexe et addictions",
            'description': "Prise en charge communautaire des troubles sévères.",
            'contenu': textwrap.dedent("""
                Troubles psychotiques, troubles de personnalité, addictions, comorbidités somatiques,
                coordination avec les structures spécialisées et inclusion sociale.
            """).strip(),
            'date_debut': datetime.date(2027, 12, 16),
            'date_fin': datetime.date(2028, 2, 15),
            'volume_horaire': 30,
        },
        {
            'code': 'DES-A3-C3',
            'classe_code': 'DES-A3',
            'ordre': 3,
            'titre': "Leadership communautaire et promotion de la santé",
            'description': "Planification et pilotage d'actions communautaires.",
            'contenu': textwrap.dedent("""
                Analyse des déterminants de santé, conception de projets communautaires,
                évaluation d'impact, plaidoyer auprès des décideurs et mobilisation sociale.
            """).strip(),
            'date_debut': datetime.date(2028, 2, 16),
            'date_fin': datetime.date(2028, 3, 31),
            'volume_horaire': 30,
        },
        {
            'code': 'DES-A3-C4',
            'classe_code': 'DES-A3',
            'ordre': 4,
            'titre': "Coordination intersectorielle des soins",
            'description': "Réseaux de soins, références et contre-références.",
            'contenu': textwrap.dedent("""
                Construction de parcours patients, coordination avec les services sociaux,
                dispositifs de télémédecine, partage d'information sécurisée.
            """).strip(),
            'date_debut': datetime.date(2028, 4, 1),
            'date_fin': datetime.date(2028, 5, 15),
            'volume_horaire': 25,
        },
        {
            'code': 'DES-A3-C5',
            'classe_code': 'DES-A3',
            'ordre': 5,
            'titre': "Méthodologie de recherche-action",
            'description': "Démarche scientifique ancrée dans la pratique communautaire.",
            'contenu': textwrap.dedent("""
                Formulation de questions de recherche, méthodes mixtes, collecte et analyse de données,
                restitution aux partenaires communautaires.
            """).strip(),
            'date_debut': datetime.date(2028, 5, 16),
            'date_fin': datetime.date(2028, 7, 15),
            'volume_horaire': 30,
        },
        {
            'code': 'DES-A3-C6',
            'classe_code': 'DES-A3',
            'ordre': 6,
            'titre': "Qualité, indicateurs et audit clinique",
            'description': "Amélioration continue de la qualité en première ligne.",
            'contenu': textwrap.dedent("""
                Construction d'indicateurs, audits cliniques, plans d'amélioration, retours d'expérience
                et culture de la sécurité des patients.
            """).strip(),
            'date_debut': datetime.date(2028, 7, 16),
            'date_fin': datetime.date(2028, 8, 31),
            'volume_horaire': 20,
        },
        # Année 4
        {
            'code': 'DES-A4-C1',
            'classe_code': 'DES-A4',
            'ordre': 1,
            'titre': "Compétences cliniques avancées",
            'description': "Cas complexes et expertise en MF/MC.",
            'contenu': textwrap.dedent("""
                Gestion des pathologies rares, protocoles avancés, supervision différée et autonomie clinique
                dans un CSCOM non universitaire.
            """).strip(),
            'date_debut': datetime.date(2028, 10, 1),
            'date_fin': datetime.date(2028, 12, 15),
            'volume_horaire': 35,
        },
        {
            'code': 'DES-A4-C2',
            'classe_code': 'DES-A4',
            'ordre': 2,
            'titre': "Supervision clinique et pédagogie",
            'description': "Encadrement des étudiants et relais communautaires.",
            'contenu': textwrap.dedent("""
                Techniques de supervision, feedback constructif, planification pédagogique,
                renforcement des compétences des équipes en place.
            """).strip(),
            'date_debut': datetime.date(2028, 12, 16),
            'date_fin': datetime.date(2029, 2, 15),
            'volume_horaire': 25,
        },
        {
            'code': 'DES-A4-C3',
            'classe_code': 'DES-A4',
            'ordre': 3,
            'titre': "Gestion stratégique des services de santé",
            'description': "Pilotage institutionnel et gouvernance.",
            'contenu': textwrap.dedent("""
                Élaboration de plans stratégiques, gestion budgétaire, négociation avec les partenaires,
                alignement avec les politiques nationales de santé.
            """).strip(),
            'date_debut': datetime.date(2029, 2, 16),
            'date_fin': datetime.date(2029, 4, 15),
            'volume_horaire': 30,
        },
        {
            'code': 'DES-A4-C4',
            'classe_code': 'DES-A4',
            'ordre': 4,
            'titre': "Préparation du mémoire et recherche clinique",
            'description': "Accompagnement méthodologique et rédaction scientifique.",
            'contenu': textwrap.dedent("""
                Analyse des données, rédaction scientifique, préparation de la soutenance,
                diffusion des résultats auprès des parties prenantes.
            """).strip(),
            'date_debut': datetime.date(2029, 4, 16),
            'date_fin': datetime.date(2029, 6, 15),
            'volume_horaire': 28,
        },
        {
            'code': 'DES-A4-C5',
            'classe_code': 'DES-A4',
            'ordre': 5,
            'titre': "Stage autonomie et transfert de compétences",
            'description': "Synthèse des acquis et préparation à l'exercice autonome.",
            'contenu': textwrap.dedent("""
                Projet personnel de fin de formation, évaluation 360°, transfert des activités aux équipes
                locales et plan de développement professionnel continu.
            """).strip(),
            'date_debut': datetime.date(2029, 6, 16),
            'date_fin': datetime.date(2029, 8, 31),
            'volume_horaire': 15,
        },
    ]

    courses_map = {}
    for data in courses_data:
        classe = classes_map[data['classe_code']]
        cours, _ = Cours.objects.get_or_create(
            classe=classe,
            code=data['code'],
            defaults={
                'titre': data['titre'],
                'description': data['description'],
                'contenu': data['contenu'],
                'date_debut': data['date_debut'],
                'date_fin': data['date_fin'],
                'volume_horaire': data['volume_horaire'],
                'ordre': data['ordre'],
            },
        )
        cours.titre = data['titre']
        cours.description = data['description']
        cours.contenu = data['contenu']
        cours.date_debut = data['date_debut']
        cours.date_fin = data['date_fin']
        cours.volume_horaire = data['volume_horaire']
        cours.ordre = data['ordre']
        cours.actif = True
        cours.save()
        courses_map[data['code']] = cours

    # ------------------------------------------------------------------
    # Jalons (semestres ou années)
    # ------------------------------------------------------------------
    jalons_data = [
        # Année 1
        {
            'code': 'DES-Y1',
            'nom': "Année 1 - Internat rotatoire MF/MC",
            'annee': 1,
            'semestre': None,
            'ordre': 1,
            'date_debut': datetime.date(2025, 10, 1),
            'date_fin': datetime.date(2026, 9, 30),
            'volume_horaire_total': 144,
            'description': textwrap.dedent("""
                Six mois de résidanat rotatoire hospitalier complétés par des modules théoriques
                ciblant les compétences fondamentales en pédiatrie, périnatalité, santé mentale,
                urgences, adultes, gériatrie et communication.
            """).strip(),
        },
        # Année 2
        {
            'code': 'DES-Y2-S1',
            'nom': "Année 2 - Semestre 1 CSCOM-U urbain",
            'annee': 2,
            'semestre': 1,
            'ordre': 1,
            'date_debut': datetime.date(2026, 10, 1),
            'date_fin': datetime.date(2027, 3, 31),
            'volume_horaire_total': 90,
            'description': textwrap.dedent("""
                Immersion en CSCOM universitaire urbain : organisation des services, coordination
                avec les structures de référence, mise en œuvre des programmes de prévention
                et consolidation des compétences de communication avancée.
            """).strip(),
        },
        {
            'code': 'DES-Y2-S2',
            'nom': "Année 2 - Semestre 2 CSCOM-U rural",
            'annee': 2,
            'semestre': 2,
            'ordre': 2,
            'date_debut': datetime.date(2027, 4, 1),
            'date_fin': datetime.date(2027, 9, 30),
            'volume_horaire_total': 75,
            'description': textwrap.dedent("""
                Immersion en CSCOM universitaire rural : adaptation aux réalités de terrain,
                renforcement des compétences en urgences périphériques et gestion opérationnelle
                complète d'un centre de santé communautaire.
            """).strip(),
        },
        # Année 3
        {
            'code': 'DES-Y3-S1',
            'nom': "Année 3 - Semestre 1 Consolidation clinique",
            'annee': 3,
            'semestre': 1,
            'ordre': 1,
            'date_debut': datetime.date(2027, 10, 1),
            'date_fin': datetime.date(2028, 3, 31),
            'volume_horaire_total': 100,
            'description': textwrap.dedent("""
                Approfondissement clinique en maladies chroniques, santé mentale complexe
                et leadership communautaire, en alternance entre CSCOM-U urbain et rural.
            """).strip(),
        },
        {
            'code': 'DES-Y3-S2',
            'nom': "Année 3 - Semestre 2 Coordination et recherche",
            'annee': 3,
            'semestre': 2,
            'ordre': 2,
            'date_debut': datetime.date(2028, 4, 1),
            'date_fin': datetime.date(2028, 9, 30),
            'volume_horaire_total': 75,
            'description': textwrap.dedent("""
                Coordination intersectorielle, recherche-action, audit clinique et amélioration continue
                de la qualité en première ligne.
            """).strip(),
        },
        # Année 4
        {
            'code': 'DES-Y4-S1',
            'nom': "Année 4 - Semestre 1 Expertise clinique",
            'annee': 4,
            'semestre': 1,
            'ordre': 1,
            'date_debut': datetime.date(2028, 10, 1),
            'date_fin': datetime.date(2029, 3, 31),
            'volume_horaire_total': 90,
            'description': textwrap.dedent("""
                Développement de compétences cliniques avancées, supervision des équipes et
                gestion stratégique des services dans un CSCOM non universitaire.
            """).strip(),
        },
        {
            'code': 'DES-Y4-S2',
            'nom': "Année 4 - Semestre 2 Autonomie et mémoire",
            'annee': 4,
            'semestre': 2,
            'ordre': 2,
            'date_debut': datetime.date(2029, 4, 1),
            'date_fin': datetime.date(2029, 9, 30),
            'volume_horaire_total': 43,
            'description': textwrap.dedent("""
                Préparation et soutenance du mémoire, projet de fin de formation et transfert
                des compétences auprès des équipes locales.
            """).strip(),
        },
    ]

    jalons_map = {}
    for data in jalons_data:
        jalon, _ = JalonProgramme.objects.get_or_create(
            formation=formation,
            code=data['code'],
            defaults={
                'nom': data['nom'],
                'annee': data['annee'],
                'semestre': data['semestre'],
                'ordre': data['ordre'],
                'description': data['description'],
                'date_debut': data['date_debut'],
                'date_fin': data['date_fin'],
                'volume_horaire_total': data['volume_horaire_total'],
            },
        )
        jalon.nom = data['nom']
        jalon.annee = data['annee']
        jalon.semestre = data['semestre']
        jalon.ordre = data['ordre']
        jalon.description = data['description']
        jalon.date_debut = data['date_debut']
        jalon.date_fin = data['date_fin']
        jalon.volume_horaire_total = data['volume_horaire_total']
        jalon.save()
        jalons_map[data['code']] = jalon

    # ------------------------------------------------------------------
    # Modules du programme et rattachement aux cours
    # ------------------------------------------------------------------
    modules_data = [
        # Jalons Année 1
        {
            'jalon_code': 'DES-Y1',
            'code': 'Y1-M1',
            'ordre': 1,
            'nom': "Rotations hospitalières fondamentales",
            'description': textwrap.dedent("""
                Médecine interne, chirurgie générale, pédiatrie, gynéco-obstétrique, psychiatrie,
                urgences et soins aux personnes âgées selon le calendrier de l'internat rotatoire.
            """).strip(),
            'volume_horaire': 0,
            'competences': [
                'expert_medical', 'professionnel',
            ],
            'courses': [],
        },
        {
            'jalon_code': 'DES-Y1',
            'code': 'Y1-M2',
            'ordre': 2,
            'nom': "Expertise clinique de l'enfant et de la femme",
            'description': "Consolidation pédiatrique et périnatale pour la pratique de première ligne.",
            'volume_horaire': 35,
            'competences': ['expert_medical'],
            'courses': ['DES-A1-C1', 'DES-A1-C2'],
        },
        {
            'jalon_code': 'DES-Y1',
            'code': 'Y1-M3',
            'ordre': 3,
            'nom': "Santé mentale en première ligne",
            'description': "Repérage, traitement et accompagnement des troubles psychiatriques courants.",
            'volume_horaire': 20,
            'competences': ['expert_medical', 'communicateur', 'professionnel'],
            'courses': ['DES-A1-C3'],
        },
        {
            'jalon_code': 'DES-Y1',
            'code': 'Y1-M4',
            'ordre': 4,
            'nom': "Urgences et habiletés techniques initiales",
            'description': "Maîtrise des situations critiques et des gestes techniques essentiels.",
            'volume_horaire': 51,
            'competences': ['expert_medical'],
            'courses': ['DES-A1-C4', 'DES-A1-C5'],
        },
        {
            'jalon_code': 'DES-Y1',
            'code': 'Y1-M5',
            'ordre': 5,
            'nom': "Soins aux adultes, gériatrie et fin de vie",
            'description': "Approche intégrée des patients adultes, âgés et en soins palliatifs.",
            'volume_horaire': 30,
            'competences': ['expert_medical'],
            'courses': ['DES-A1-C6', 'DES-A1-C7'],
        },
        {
            'jalon_code': 'DES-Y1',
            'code': 'Y1-M6',
            'ordre': 6,
            'nom': "Compétences transversales",
            'description': "Communication thérapeutique, collaboration et éthique clinique.",
            'volume_horaire': 8,
            'competences': ['communicateur', 'collaborateur', 'professionnel'],
            'courses': ['DES-A1-C8'],
        },
        # Jalons Année 2
        {
            'jalon_code': 'DES-Y2-S1',
            'code': 'Y2S1-M1',
            'ordre': 1,
            'nom': "Immersion CSCOM-U urbain",
            'description': "Organisation des soins, flux patients et continuité des services urbains.",
            'volume_horaire': 40,
            'competences': ['expert_medical', 'promoteur', 'gestionnaire'],
            'courses': ['DES-A2-C1'],
        },
        {
            'jalon_code': 'DES-Y2-S1',
            'code': 'Y2S1-M2',
            'ordre': 2,
            'nom': "Programmes nationaux et prévention",
            'description': "Mise en œuvre des programmes de santé publique en milieu urbain.",
            'volume_horaire': 25,
            'competences': ['promoteur', 'gestionnaire'],
            'courses': ['DES-A2-C3'],
        },
        {
            'jalon_code': 'DES-Y2-S1',
            'code': 'Y2S1-M3',
            'ordre': 3,
            'nom': "Communication et collaboration avancées",
            'description': "Mobilisation des acteurs institutionnels et communautaires urbains.",
            'volume_horaire': 25,
            'competences': ['communicateur', 'collaborateur', 'professionnel'],
            'courses': ['DES-A2-C4'],
        },
        {
            'jalon_code': 'DES-Y2-S2',
            'code': 'Y2S2-M1',
            'ordre': 1,
            'nom': "Immersion CSCOM-U rural",
            'description': "Soins essentiels et coordination des ressources en zone rurale.",
            'volume_horaire': 40,
            'competences': ['expert_medical', 'promoteur', 'gestionnaire'],
            'courses': ['DES-A2-C2'],
        },
        {
            'jalon_code': 'DES-Y2-S2',
            'code': 'Y2S2-M2',
            'ordre': 2,
            'nom': "Urgences et obstétrique périphériques",
            'description': "Stabilisation et transferts sécuritaires dans des contextes à ressources limitées.",
            'volume_horaire': 20,
            'competences': ['expert_medical', 'professionnel'],
            'courses': ['DES-A2-C5'],
        },
        {
            'jalon_code': 'DES-Y2-S2',
            'code': 'Y2S2-M3',
            'ordre': 3,
            'nom': "Gestion opérationnelle du CSCOM",
            'description': "Administration, finances, ressources humaines et logistique.",
            'volume_horaire': 15,
            'competences': ['gestionnaire', 'professionnel'],
            'courses': ['DES-A2-C6'],
        },
        # Jalons Année 3
        {
            'jalon_code': 'DES-Y3-S1',
            'code': 'Y3S1-M1',
            'ordre': 1,
            'nom': "Gestion des maladies chroniques",
            'description': "Organisation du suivi longitudinal et coordination spécialisée.",
            'volume_horaire': 40,
            'competences': ['expert_medical', 'promoteur'],
            'courses': ['DES-A3-C1'],
        },
        {
            'jalon_code': 'DES-Y3-S1',
            'code': 'Y3S1-M2',
            'ordre': 2,
            'nom': "Santé mentale complexe",
            'description': "Prise en charge communautaire des troubles sévères et addictions.",
            'volume_horaire': 30,
            'competences': ['expert_medical', 'communicateur', 'collaborateur'],
            'courses': ['DES-A3-C2'],
        },
        {
            'jalon_code': 'DES-Y3-S1',
            'code': 'Y3S1-M3',
            'ordre': 3,
            'nom': "Leadership communautaire et promotion",
            'description': "Conception et pilotage de projets communautaires innovants.",
            'volume_horaire': 30,
            'competences': ['promoteur', 'gestionnaire', 'professionnel'],
            'courses': ['DES-A3-C3'],
        },
        {
            'jalon_code': 'DES-Y3-S2',
            'code': 'Y3S2-M1',
            'ordre': 1,
            'nom': "Coordination intersectorielle",
            'description': "Construction de parcours patients et intégration des services sociaux.",
            'volume_horaire': 25,
            'competences': ['collaborateur', 'communicateur', 'gestionnaire'],
            'courses': ['DES-A3-C4'],
        },
        {
            'jalon_code': 'DES-Y3-S2',
            'code': 'Y3S2-M2',
            'ordre': 2,
            'nom': "Recherche-action en MF/MC",
            'description': "Méthodes et diffusion de la recherche appliquée à la communauté.",
            'volume_horaire': 30,
            'competences': ['erudit', 'promoteur', 'professionnel'],
            'courses': ['DES-A3-C5'],
        },
        {
            'jalon_code': 'DES-Y3-S2',
            'code': 'Y3S2-M3',
            'ordre': 3,
            'nom': "Qualité, indicateurs et audit",
            'description': "Amélioration continue et culture de la sécurité des patients.",
            'volume_horaire': 20,
            'competences': ['gestionnaire', 'professionnel'],
            'courses': ['DES-A3-C6'],
        },
        # Jalons Année 4
        {
            'jalon_code': 'DES-Y4-S1',
            'code': 'Y4S1-M1',
            'ordre': 1,
            'nom': "Compétences cliniques avancées",
            'description': "Cas complexes et expertise clinique en autonomie supervisée.",
            'volume_horaire': 35,
            'competences': ['expert_medical'],
            'courses': ['DES-A4-C1'],
        },
        {
            'jalon_code': 'DES-Y4-S1',
            'code': 'Y4S1-M2',
            'ordre': 2,
            'nom': "Supervision clinique et pédagogie",
            'description': "Encadrement des étudiants, relais communautaires et équipes.",
            'volume_horaire': 25,
            'competences': ['communicateur', 'collaborateur', 'professionnel'],
            'courses': ['DES-A4-C2'],
        },
        {
            'jalon_code': 'DES-Y4-S1',
            'code': 'Y4S1-M3',
            'ordre': 3,
            'nom': "Gestion stratégique des services",
            'description': "Pilotage institutionnel, gouvernance et négociation des ressources.",
            'volume_horaire': 30,
            'competences': ['gestionnaire', 'professionnel'],
            'courses': ['DES-A4-C3'],
        },
        {
            'jalon_code': 'DES-Y4-S2',
            'code': 'Y4S2-M1',
            'ordre': 1,
            'nom': "Mémoire et recherche clinique",
            'description': "Analyse des données, rédaction et soutenance du mémoire.",
            'volume_horaire': 28,
            'competences': ['erudit', 'professionnel'],
            'courses': ['DES-A4-C4'],
        },
        {
            'jalon_code': 'DES-Y4-S2',
            'code': 'Y4S2-M2',
            'ordre': 2,
            'nom': "Autonomie professionnelle et transfert",
            'description': "Projet final, plan de développement continu et transfert de compétences.",
            'volume_horaire': 15,
            'competences': ['professionnel', 'collaborateur', 'gestionnaire'],
            'courses': ['DES-A4-C5'],
        },
    ]

    for mod_data in modules_data:
        jalon = jalons_map[mod_data['jalon_code']]
        module, _ = ModuleProgramme.objects.get_or_create(
            jalon=jalon,
            code=mod_data['code'],
            defaults={
                'nom': mod_data['nom'],
                'description': mod_data['description'],
                'volume_horaire': mod_data['volume_horaire'],
                'ordre': mod_data['ordre'],
                'actif': True,
            },
        )
        module.nom = mod_data['nom']
        module.description = mod_data['description']
        module.volume_horaire = mod_data['volume_horaire']
        module.ordre = mod_data['ordre']
        module.actif = True
        module.save()

        # Mise à jour des compétences associées
        competence_objs = [competences_map[key] for key in mod_data.get('competences', [])]
        module.competences_module.set(competence_objs)

        # Synchronisation des cours du module
        desired_course_codes = mod_data.get('courses', [])
        module.cours_programme.exclude(cours__code__in=desired_course_codes).delete()

        for order_index, course_code in enumerate(desired_course_codes, start=1):
            course = courses_map[course_code]
            cours_prog, _ = CoursProgramme.objects.get_or_create(
                module=module,
                cours=course,
                defaults={
                    'ordre': order_index,
                    'obligatoire': True,
                },
            )
            cours_prog.ordre = order_index
            cours_prog.obligatoire = True
            cours_prog.save()


def unseed_desmfmc_programme(apps, schema_editor):
    Formation = apps.get_model('utilisateurs', 'Formation')
    Classe = apps.get_model('utilisateurs', 'Classe')
    Cours = apps.get_model('utilisateurs', 'Cours')
    Competence = apps.get_model('utilisateurs', 'Competence')
    JalonProgramme = apps.get_model('utilisateurs', 'JalonProgramme')
    ModuleProgramme = apps.get_model('utilisateurs', 'ModuleProgramme')
    CoursProgramme = apps.get_model('utilisateurs', 'CoursProgramme')

    formation = Formation.objects.filter(code='DESMFMC').first()
    if not formation:
        return

    module_codes = [  # mêmes codes que dans seed
        'Y1-M1', 'Y1-M2', 'Y1-M3', 'Y1-M4', 'Y1-M5', 'Y1-M6',
        'Y2S1-M1', 'Y2S1-M2', 'Y2S1-M3', 'Y2S2-M1', 'Y2S2-M2', 'Y2S2-M3',
        'Y3S1-M1', 'Y3S1-M2', 'Y3S1-M3', 'Y3S2-M1', 'Y3S2-M2', 'Y3S2-M3',
        'Y4S1-M1', 'Y4S1-M2', 'Y4S1-M3', 'Y4S2-M1', 'Y4S2-M2',
    ]
    jalon_codes = ['DES-Y1', 'DES-Y2-S1', 'DES-Y2-S2', 'DES-Y3-S1', 'DES-Y3-S2', 'DES-Y4-S1', 'DES-Y4-S2']
    course_codes = [data['code'] for data in [
        # même séquence que seed (simplifié pour lecture)
        {'code': 'DES-A1-C1'}, {'code': 'DES-A1-C2'}, {'code': 'DES-A1-C3'}, {'code': 'DES-A1-C4'},
        {'code': 'DES-A1-C5'}, {'code': 'DES-A1-C6'}, {'code': 'DES-A1-C7'}, {'code': 'DES-A1-C8'},
        {'code': 'DES-A2-C1'}, {'code': 'DES-A2-C2'}, {'code': 'DES-A2-C3'}, {'code': 'DES-A2-C4'},
        {'code': 'DES-A2-C5'}, {'code': 'DES-A2-C6'},
        {'code': 'DES-A3-C1'}, {'code': 'DES-A3-C2'}, {'code': 'DES-A3-C3'}, {'code': 'DES-A3-C4'},
        {'code': 'DES-A3-C5'}, {'code': 'DES-A3-C6'},
        {'code': 'DES-A4-C1'}, {'code': 'DES-A4-C2'}, {'code': 'DES-A4-C3'}, {'code': 'DES-A4-C4'},
        {'code': 'DES-A4-C5'},
    ]]
    classe_codes = ['DES-A1', 'DES-A2', 'DES-A3', 'DES-A4']
    competence_libelles = [
        "Expert médical en MF/MC",
        "Communicateur",
        "Collaborateur",
        "Promoteur de la santé",
        "Gestionnaire",
        "Professionnel",
        "Érudit",
    ]

    modules_qs = ModuleProgramme.objects.filter(jalon__formation=formation, code__in=module_codes)
    CoursProgramme.objects.filter(module__in=modules_qs).delete()
    modules_qs.delete()

    JalonProgramme.objects.filter(formation=formation, code__in=jalon_codes).delete()
    Cours.objects.filter(classe__formation=formation, code__in=course_codes).delete()
    Classe.objects.filter(formation=formation, code__in=classe_codes).delete()

    # Supprimer les compétences ajoutées si elles ne sont plus liées à d'autres modules
    Competence.objects.filter(libelle__in=competence_libelles, modules__isnull=True).delete()

    # Si la formation n'a plus de jalons ni de classes, on peut éventuellement la supprimer
    if not formation.jalons.exists() and not formation.classes.exists():
        formation.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0005_alter_utilisateur_options_alter_utilisateur_groups_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_desmfmc_programme, unseed_desmfmc_programme),
    ]


