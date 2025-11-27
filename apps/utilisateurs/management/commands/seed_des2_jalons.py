"""
Commande de seed pour les jalons, cours et leçons de la DEUXIÈME ANNÉE uniquement du DESMFMC.

⚠️  IMPORTANT: Cette commande est réservée à la classe DES-A2 (année 2) uniquement.
Pour les années 1, 3 et 4, utiliser les commandes correspondantes.

Source des données: Programme DESMFMC - Année 2
"""
import datetime
import textwrap

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.utilisateurs.models_formation import (
    Formation,
    Classe,
    Cours,
    Lecon,
    Competence,
    CompetenceJalon,
)


# ⚠️  DONNÉES UNIQUEMENT POUR LA DEUXIÈME ANNÉE (DES-A2)
DES2_JALONS_DATA = [
    {
        "competence": "Expert médical en MF/MC",
        "classe_code": "DES-A2",
        "titre": "Expert médical – Soins courants aux enfants, soins périnataux et soins de première ligne (milieu urbain)",
        "ordre": 10,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Expert médical en milieu urbain (année 2) :
            
            - Démontre un bon niveau de connaissances théoriques et cliniques dans l'évaluation et les soins qu'il prodigue aux patients en particulier au niveau des soins aux enfants, soins périnataux et soins courants en première ligne.
            
            - Recueille les données cliniques pertinentes en fonction des différentes hypothèses diagnostiques à considérer.
            
            - Évalue les problèmes de façon globale et centrée sur le patient et adapte son approche en tenant compte de la culture, des caractéristiques du milieu et des ressources du CSCOM.
            
            - Effectue adéquatement l'examen physique et les gestes techniques en s'assurant du confort du patient principalement en lien avec les soins courants, les soins aux enfants et en périnatalité.
            
            - Interprète justement les données en tenant compte de l'ensemble de la situation.
            
            - Choisit un plan d'intervention approprié (investigation, traitement, suivi, transfert) en tenant compte du point de vue et des ressources du patient.
            
            - Assurer un accouchement eutocique.
            
            - Réaliser une CPN, CPON.
            
            - Dépister une grossesse à risque.
            
            - Diagnostiquer une urgence obstétricale.
            
            - Assurer la PTME.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A2-PED",
                "ordre": 1,
                "titre": "Pédiatrie - Soins courants aux enfants",
                "volume_horaire": 20,
                "description": "Cours sur les soins courants aux enfants en première ligne (20h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge des problèmes de santé courants chez l'enfant :
                    maladies fébriles, infections fréquentes, retards de développement,
                    pleurs excessifs, troubles digestifs et alimentaires, problèmes locomoteurs,
                    troubles du sommeil, troubles de l'ouïe et de la parole.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 1, "titre": "Maladies fébriles", "type": "lecon"},
                    {"numero": 2, "titre": "Infections fréquentes", "type": "lecon"},
                    {"numero": 3, "titre": "Retard de développement staturo-pondéral et psychomoteur", "type": "lecon"},
                    {"numero": 4, "titre": "Pleurs excessifs", "type": "lecon"},
                    {"numero": 5, "titre": "Troubles digestifs et alimentaires fréquents", "type": "lecon"},
                    {"numero": 6, "titre": "Problèmes locomoteurs", "type": "lecon"},
                    {"numero": 7, "titre": "Troubles du sommeil", "type": "lecon"},
                    {"numero": 8, "titre": "Troubles de l'ouïe et de la parole", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A2-OBS",
                "ordre": 2,
                "titre": "Obstétrique - Grossesse, accouchement et allaitement",
                "volume_horaire": 15,
                "description": "Cours sur la grossesse, l'accouchement et l'allaitement en première ligne (15h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge obstétricale de première ligne :
                    planification familiale, suivi des grossesses (normales, à risques et pathologiques),
                    techniques obstétricales, dystocies, infections et grossesse.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 9, "titre": "Planification familiale (PF)", "type": "lecon"},
                    {"numero": 10, "titre": "Suivi des grossesses (normales, à risques et pathologiques)", "type": "lecon"},
                    {"numero": 11, "titre": "Techniques obstétricales", "type": "lecon"},
                    {"numero": 12, "titre": "Dystocies", "type": "lecon"},
                    {"numero": 13, "titre": "Infections et grossesse", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A2-URG-OBS",
                "ordre": 3,
                "titre": "Urgences obstétricales",
                "volume_horaire": 27,
                "description": "Cours sur les urgences obstétricales sous forme d'ateliers pratiques (27h).",
                "contenu": textwrap.dedent(
                    """
                    Gestion des urgences obstétricales en première ligne :
                    hémorragies du post-partum, réanimation du nouveau-né.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 14, "titre": "Gestion des hémorragies du post-partum", "type": "atelier"},
                    {"numero": 15, "titre": "Réanimation du nouveau-né", "type": "atelier"},
                ],
            },
            {
                "code": "DES-A2-CHIR",
                "ordre": 4,
                "titre": "Chirurgie générale",
                "volume_horaire": 35,
                "description": "Cours de chirurgie générale sous forme d'ateliers pratiques FIRST (35h).",
                "contenu": textwrap.dedent(
                    """
                    Habiletés chirurgicales de première ligne (FIRST - Fundamental Invasive and Resuscitative Skills Training) :
                    techniques chirurgicales essentielles pour la pratique en première ligne.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 16, "titre": "Chirurgicaux (FIRST)", "type": "atelier"},
                ],
            },
            {
                "code": "DES-A2-GYN",
                "ordre": 5,
                "titre": "Gynécologie - Soins aux femmes et aux adolescentes",
                "volume_horaire": 20,
                "description": "Cours sur les soins gynécologiques aux femmes et aux adolescentes en première ligne (20h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge gynécologique de première ligne :
                    infertilité, infections sexuellement transmissibles, dysménorrhées, métrorragies,
                    tumeurs pelviennes, maladies du sein, violences et abus sexuels, ménopause,
                    ostéoporose, gestion des MGF/E, dépistage du cancer du col de l'utérus.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 17, "titre": "L'infertilité", "type": "lecon"},
                    {"numero": 18, "titre": "Les infections sexuellement transmissibles", "type": "lecon"},
                    {"numero": 19, "titre": "Les dysménorrhées", "type": "lecon"},
                    {"numero": 20, "titre": "Les métrorragies", "type": "lecon"},
                    {"numero": 21, "titre": "Les tumeurs pelviennes", "type": "lecon"},
                    {"numero": 22, "titre": "Les maladies du sein", "type": "lecon"},
                    {"numero": 23, "titre": "Violences et abus sexuels", "type": "lecon"},
                    {"numero": 24, "titre": "La ménopause", "type": "lecon"},
                    {"numero": 25, "titre": "L'ostéoporose", "type": "lecon"},
                    {"numero": 26, "titre": "Gestion des MGF/E", "type": "lecon"},
                    {"numero": 27, "titre": "Technique de dépistage du cancer du col de l'utérus", "type": "atelier"},
                ],
            },
        ],
    },
    {
        "competence": "Communicateur",
        "classe_code": "DES-A2",
        "titre": "Communicateur – Relation thérapeutique et communication en milieu urbain",
        "ordre": 20,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Communicateur en milieu urbain (année 2) :
            
            - Démontre des habiletés relationnelles et de communication empreintes d'empathie et de respect avec les patients et leur famille.
            
            - Transmet clairement les informations médicales aux patients et à leur famille dans un langage adapté.
            
            - Rédige les documents médicaux de façon claire et pertinente (dossier ou fiche de référence et d'évacuation du patient).
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A2-COMM",
                "ordre": 1,
                "titre": "Technique de communication",
                "volume_horaire": 18,
                "description": "Cours sur les techniques de communication thérapeutique en première ligne (18h).",
                "contenu": textwrap.dedent(
                    """
                    Développement des compétences en communication thérapeutique :
                    entrevue du malade, approche des adolescents, techniques de début et fin d'entrevue.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 24, "titre": "L'entrevue du malade", "type": "lecon"},
                    {"numero": 25, "titre": "Particularité de l'approche des adolescents (es)", "type": "lecon"},
                    {"numero": 4, "titre": "Début d'entrevue", "type": "atelier"},
                    {"numero": 5, "titre": "Fin d'entrevue", "type": "atelier"},
                ],
            },
        ],
    },
    {
        "competence": "Promoteur de la santé",
        "classe_code": "DES-A2",
        "titre": "Promoteur de la santé – Programmes nationaux et prévention en milieu urbain",
        "ordre": 30,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Promoteur de la santé en milieu urbain (année 2) :
            
            - Démontre qu'il connaît les recommandations des programmes nationaux lors des rencontres de planification et d'organisation des séances de vaccination, rencontres de formation avec les relais, causeries éducatives.
            
            - Identifie les facteurs de risque et de récidive de certaines pathologies lors des consultations et des visites de milieu avec les relais.
            
            - Inclut systématiquement dans ses consultations les recommandations de dépistage et de guidance quant à la malnutrition, infections respiratoires, maladies diarrhéiques, paludisme, VIH-SIDA, IST.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A2-PED-SUIVI",
                "ordre": 1,
                "titre": "Pédiatrie - Suivi de l'enfant",
                "volume_horaire": 15,
                "description": "Cours sur le suivi de l'enfant et les programmes de prévention en première ligne (15h).",
                "contenu": textwrap.dedent(
                    """
                    Suivi de l'enfant et prévention :
                    examen périodique et vaccination, conseils nutritionnels, consultation post-natale,
                    méthodes de changement et modification des habitudes de vie.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 26, "titre": "Examen périodique et vaccination", "type": "lecon"},
                    {"numero": 27, "titre": "Conseils nutrition", "type": "lecon"},
                    {"numero": 28, "titre": "Consultation post-natale", "type": "lecon"},
                    {"numero": 29, "titre": "Examen périodique", "type": "lecon"},
                    {"numero": 30, "titre": "Méthodes de changement et modification des habitudes de vie", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Gestionnaire",
        "classe_code": "DES-A2",
        "titre": "Gestionnaire – Gestion des services et planification en milieu urbain",
        "ordre": 40,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Gestionnaire en milieu urbain (année 2) :
            
            - Peut expliquer le fonctionnement et le rôle des ASACO dans l'organisation des services et la prestation des soins.
            
            - Participe activement aux différents comités d'évaluation de l'exercice professionnel et aux activités de monitorage.
            
            - Contribue à l'élaboration et à l'implantation des stratégies avancées et du micro plan sanitaire.
            
            - Démontre des connaissances de base en comptabilité dans la planification des inventaires et dans les différents rapports produits pour le CSCOM.
            
            - Élaborer un plan opérationnel annuel du CSCom.
            
            - Élaborer et utiliser un tableau de bord des indicateurs du PEV.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A2-GEST",
                "ordre": 1,
                "titre": "Gestion - Gestion des données",
                "volume_horaire": 10,
                "description": "Cours sur la gestion des données et la planification en première ligne (10h).",
                "contenu": textwrap.dedent(
                    """
                    Gestion des données sanitaires et administratives :
                    micro-planification, comptes d'exploitation, remplissage des supports administratifs.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 31, "titre": "La micro-planification", "type": "lecon"},
                    {"numero": 32, "titre": "Comptes d'exploitation", "type": "lecon"},
                    {"numero": 33, "titre": "Remplissage des supports", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Érudit",
        "classe_code": "DES-A2",
        "titre": "Érudit – Développement professionnel continu et recherche en milieu urbain",
        "ordre": 50,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Érudit en milieu urbain (année 2) :
            
            - Contribue à l'éducation des patients, de la communauté et des différents membres de l'équipe de soins en partageant de manière adaptée son savoir (causeries éducatives, staff, formation des relais).
            
            - Fait preuve de curiosité scientifique et collabore activement au développement de ses compétences.
            
            - Applique de façon critique les données probantes selon le contexte de pratique et la réalité des patients et des communautés.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A2-METH",
                "ordre": 1,
                "titre": "Méthodologie de la recherche - Clubs de lecture",
                "volume_horaire": 10,
                "description": "Cours sur la méthodologie de la recherche et l'analyse critique de la littérature (10h).",
                "contenu": textwrap.dedent(
                    """
                    Développement des compétences en recherche et analyse critique :
                    analyse critique de la littérature médicale, niveaux de preuve, application
                    des données probantes au contexte de pratique.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 34, "titre": "Analyse critique de la littérature", "type": "lecon"},
                    {"numero": 35, "titre": "Niveaux de preuve", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Professionnel",
        "classe_code": "DES-A2",
        "titre": "Professionnel – Éthique, déontologie et compétences numériques en milieu urbain",
        "ordre": 60,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Professionnel en milieu urbain (année 2) :
            
            - Intervient avec professionnalisme et de manière éthique auprès des patients et des autres membres du réseau de soins.
            
            - Respecte les principes éthiques, légaux et déontologiques de la pratique médicale.
            
            - Démontre des compétences en informatique médicale pour la documentation et la présentation professionnelle.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A2-ETH",
                "ordre": 1,
                "titre": "Éthique et déontologie",
                "volume_horaire": 3,
                "description": "Cours sur l'éthique et la déontologie médicale (3h).",
                "contenu": textwrap.dedent(
                    """
                    Principes éthiques et déontologiques de la pratique médicale :
                    discussions éthiques, cas pratiques, réflexion sur les dilemmes éthiques en première ligne.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 36, "titre": "Discussion éthique", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A2-INFO",
                "ordre": 2,
                "titre": "Informatique médicale",
                "volume_horaire": 10,
                "description": "Cours sur l'informatique médicale et les outils de présentation (10h).",
                "contenu": textwrap.dedent(
                    """
                    Compétences en informatique médicale :
                    critères d'une bonne présentation, utilisation de Word, Excel et PowerPoint
                    pour la documentation médicale et les présentations professionnelles.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 37, "titre": "Critères d'une bonne présentation", "type": "lecon"},
                    {"numero": 38, "titre": "Word", "type": "lecon"},
                    {"numero": 39, "titre": "Excel", "type": "lecon"},
                    {"numero": 40, "titre": "PowerPoint", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Collaborateur",
        "classe_code": "DES-A2",
        "titre": "Collaborateur – Travail en équipe et collaboration interprofessionnelle en milieu urbain",
        "ordre": 25,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Collaborateur en milieu urbain (année 2) :
            
            - Reconnaît l'expertise et la contribution des autres professionnels de la santé (personnel infirmier, sages-femmes, préposée à la pharmacie) dans les soins aux patients et dans son propre apprentissage.
            
            - Sollicite de façon pertinente la collaboration de tous les acteurs (professionnels de la santé, relais, ASACO) pour optimiser la qualité des soins et services aux patients et à la population.
            
            - Communique avec l'ensemble du personnel et des professionnels de manière respectueuse et efficace.
            """
        ).strip(),
        "courses": [],
    },
    # ===================================================================
    # JALONS POUR LE MILIEU RURAL (même classe DES-A2, jalons différents)
    # ===================================================================
    {
        "competence": "Expert médical en MF/MC",
        "classe_code": "DES-A2",
        "titre": "Expert médical – Soins courants aux enfants, soins périnataux et soins de première ligne (milieu rural)",
        "ordre": 11,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Expert médical en milieu rural (année 2) :
            
            - Démontre un bon niveau de connaissances théoriques et cliniques dans l'évaluation et les soins qu'il prodigue aux patients en particulier au niveau des soins aux enfants, soins périnataux et soins courants en première ligne.
            
            - Recueille les données cliniques pertinentes en fonction des différentes hypothèses diagnostiques à considérer.
            
            - Évalue les problèmes de façon globale et centrée sur le patient et adapte son approche en tenant compte de la culture, des caractéristiques du milieu et des ressources du CSCOM.
            
            - Effectue adéquatement l'examen physique et les gestes techniques en s'assurant du confort du patient principalement en lien avec les soins courants, les soins aux enfants et en périnatalité.
            
            - Interprète justement les données en tenant compte de l'ensemble de la situation.
            
            - Choisit un plan d'intervention approprié (investigation, traitement, suivi, transfert) en tenant compte du point de vue et des ressources du patient.
            
            - Élaborer un plan d'action de riposte contre les maladies à potentiel épidémique (Rougeole, Tétanos néonatal…).
            
            - Administrer les antigènes du PEV.
            
            - Reconnaître un vaccin viré.
            """
        ).strip(),
        "courses": [
            # Réutilisation des mêmes cours que le milieu urbain (get_or_create les réutilisera)
            {
                "code": "DES-A2-PED",
                "ordre": 1,
                "titre": "Pédiatrie - Soins courants aux enfants",
                "volume_horaire": 20,
                "description": "Cours sur les soins courants aux enfants en première ligne (20h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge des problèmes de santé courants chez l'enfant :
                    maladies fébriles, infections fréquentes, retards de développement,
                    pleurs excessifs, troubles digestifs et alimentaires, problèmes locomoteurs,
                    troubles du sommeil, troubles de l'ouïe et de la parole.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 1, "titre": "Maladies fébriles", "type": "lecon"},
                    {"numero": 2, "titre": "Infections fréquentes", "type": "lecon"},
                    {"numero": 3, "titre": "Retard de développement staturo-pondéral et psychomoteur", "type": "lecon"},
                    {"numero": 4, "titre": "Pleurs excessifs", "type": "lecon"},
                    {"numero": 5, "titre": "Troubles digestifs et alimentaires fréquents", "type": "lecon"},
                    {"numero": 6, "titre": "Problèmes locomoteurs", "type": "lecon"},
                    {"numero": 7, "titre": "Troubles du sommeil", "type": "lecon"},
                    {"numero": 8, "titre": "Troubles de l'ouïe et de la parole", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A2-OBS",
                "ordre": 2,
                "titre": "Obstétrique - Grossesse, accouchement et allaitement",
                "volume_horaire": 15,
                "description": "Cours sur la grossesse, l'accouchement et l'allaitement en première ligne (15h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge obstétricale de première ligne :
                    planification familiale, suivi des grossesses (normales, à risques et pathologiques),
                    techniques obstétricales, dystocies, infections et grossesse.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 9, "titre": "Planification familiale (PF)", "type": "lecon"},
                    {"numero": 10, "titre": "Suivi des grossesses (normales, à risques et pathologiques)", "type": "lecon"},
                    {"numero": 11, "titre": "Techniques obstétricales", "type": "lecon"},
                    {"numero": 12, "titre": "Dystocies", "type": "lecon"},
                    {"numero": 13, "titre": "Infections et grossesse", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A2-URG-OBS",
                "ordre": 3,
                "titre": "Urgences obstétricales",
                "volume_horaire": 27,
                "description": "Cours sur les urgences obstétricales sous forme d'ateliers pratiques (27h).",
                "contenu": textwrap.dedent(
                    """
                    Gestion des urgences obstétricales en première ligne :
                    hémorragies du post-partum, réanimation du nouveau-né.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 14, "titre": "Gestion des hémorragies du post-partum", "type": "atelier"},
                    {"numero": 15, "titre": "Réanimation du nouveau-né", "type": "atelier"},
                ],
            },
            {
                "code": "DES-A2-CHIR",
                "ordre": 4,
                "titre": "Chirurgie générale",
                "volume_horaire": 35,
                "description": "Cours de chirurgie générale sous forme d'ateliers pratiques FIRST (35h).",
                "contenu": textwrap.dedent(
                    """
                    Habiletés chirurgicales de première ligne (FIRST - Fundamental Invasive and Resuscitative Skills Training) :
                    techniques chirurgicales essentielles pour la pratique en première ligne.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 16, "titre": "Chirurgicaux (FIRST)", "type": "atelier"},
                ],
            },
            {
                "code": "DES-A2-GYN",
                "ordre": 5,
                "titre": "Gynécologie - Soins aux femmes et aux adolescentes",
                "volume_horaire": 20,
                "description": "Cours sur les soins gynécologiques aux femmes et aux adolescentes en première ligne (20h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge gynécologique de première ligne :
                    infertilité, infections sexuellement transmissibles, dysménorrhées, métrorragies,
                    tumeurs pelviennes, maladies du sein, violences et abus sexuels, ménopause,
                    ostéoporose, gestion des MGF/E, dépistage du cancer du col de l'utérus.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 17, "titre": "L'infertilité", "type": "lecon"},
                    {"numero": 18, "titre": "Les infections sexuellement transmissibles", "type": "lecon"},
                    {"numero": 19, "titre": "Les dysménorrhées", "type": "lecon"},
                    {"numero": 20, "titre": "Les métrorragies", "type": "lecon"},
                    {"numero": 21, "titre": "Les tumeurs pelviennes", "type": "lecon"},
                    {"numero": 22, "titre": "Les maladies du sein", "type": "lecon"},
                    {"numero": 23, "titre": "Violences et abus sexuels", "type": "lecon"},
                    {"numero": 24, "titre": "La ménopause", "type": "lecon"},
                    {"numero": 25, "titre": "L'ostéoporose", "type": "lecon"},
                    {"numero": 26, "titre": "Gestion des MGF/E", "type": "lecon"},
                    {"numero": 27, "titre": "Technique de dépistage du cancer du col de l'utérus", "type": "atelier"},
                ],
            },
            {
                "code": "DES-A2-DERM",
                "ordre": 6,
                "titre": "Dermatologie",
                "volume_horaire": 15,
                "description": "Cours sur la dermatologie en première ligne (15h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge dermatologique de première ligne :
                    infections cutanées, dermatoses inflammatoires, lésions pigmentées,
                    pathologies cutanées courantes, soins des plaies.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 28, "titre": "Infections cutanées bactériennes", "type": "lecon"},
                    {"numero": 29, "titre": "Infections cutanées fongiques", "type": "lecon"},
                    {"numero": 30, "titre": "Infections cutanées virales", "type": "lecon"},
                    {"numero": 31, "titre": "Dermatoses inflammatoires (eczéma, psoriasis)", "type": "lecon"},
                    {"numero": 32, "titre": "Lésions pigmentées et tumeurs cutanées", "type": "lecon"},
                    {"numero": 33, "titre": "Pathologies cutanées courantes (gale, teigne, acné)", "type": "lecon"},
                    {"numero": 34, "titre": "Soins des plaies et ulcères", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Communicateur",
        "classe_code": "DES-A2",
        "titre": "Communicateur – Relation thérapeutique et communication en milieu rural",
        "ordre": 21,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Communicateur en milieu rural (année 2) :
            
            - Démontre des habiletés relationnelles et de communication empreintes d'empathie et de respect avec les patients et leur famille.
            
            - Transmet clairement les informations médicales aux patients et à leur famille dans un langage adapté.
            
            - Rédige les documents médicaux de façon claire et pertinente (dossier ou fiche de référence et d'évacuation du patient).
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A2-COMM",
                "ordre": 1,
                "titre": "Technique de communication",
                "volume_horaire": 18,
                "description": "Cours sur les techniques de communication thérapeutique (18h).",
                "contenu": textwrap.dedent(
                    """
                    Développement des compétences en communication :
                    entrevue du malade, approche des adolescents, techniques de début et fin d'entrevue.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 24, "titre": "L'entrevue du malade", "type": "lecon"},
                    {"numero": 25, "titre": "Particularité de l'approche des adolescents (es)", "type": "lecon"},
                    {"numero": 4, "titre": "Début d'entrevue", "type": "atelier"},
                    {"numero": 5, "titre": "Fin d'entrevue", "type": "atelier"},
                ],
            },
        ],
    },
    {
        "competence": "Collaborateur",
        "classe_code": "DES-A2",
        "titre": "Collaborateur – Travail en équipe et collaboration interprofessionnelle en milieu rural",
        "ordre": 26,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Collaborateur en milieu rural (année 2) :
            
            - Reconnaît l'expertise et la contribution des autres professionnels de la santé (personnel infirmier, sages-femmes, préposée à la pharmacie) dans les soins aux patients et dans son propre apprentissage.
            
            - Sollicite de façon pertinente la collaboration de tous les acteurs (professionnels de la santé, relais, ASACO) pour optimiser la qualité des soins et services aux patients et à la population.
            
            - Communique avec l'ensemble du personnel et des professionnels de manière respectueuse et efficace.
            """
        ).strip(),
        "courses": [],
    },
    {
        "competence": "Promoteur de la santé",
        "classe_code": "DES-A2",
        "titre": "Promoteur de la santé – Programmes nationaux et prévention en milieu rural",
        "ordre": 31,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Promoteur de la santé en milieu rural (année 2) :
            
            - Démontre qu'il connaît les recommandations des programmes nationaux lors des rencontres de planification et d'organisation des séances de vaccination, rencontres de formation avec les relais, causeries éducatives.
            
            - Identifie les facteurs de risque et de récidive de certaines pathologies lors des consultations et des visites de milieu avec les relais.
            
            - Inclut systématiquement dans ses consultations les recommandations de dépistage et de guidance quant à la malnutrition, infections respiratoires, maladies diarrhéiques, paludisme, VIH-SIDA, IST.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A2-PED-SUIVI",
                "ordre": 1,
                "titre": "Pédiatrie - Suivi de l'enfant",
                "volume_horaire": 15,
                "description": "Cours sur le suivi de l'enfant et les programmes de prévention (15h).",
                "contenu": textwrap.dedent(
                    """
                    Suivi de l'enfant et prévention :
                    examen périodique et vaccination, conseils nutrition, consultation post-natale,
                    examen périodique, méthodes de changement et modification des habitudes de vie.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 26, "titre": "Examen périodique et vaccination", "type": "lecon"},
                    {"numero": 27, "titre": "Conseils nutrition", "type": "lecon"},
                    {"numero": 28, "titre": "Consultation Post natale", "type": "lecon"},
                    {"numero": 29, "titre": "Examen périodique", "type": "lecon"},
                    {"numero": 30, "titre": "Méthodes de changement et modification des habitudes de vie", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Gestionnaire",
        "classe_code": "DES-A2",
        "titre": "Gestionnaire – Gestion des services et planification en milieu rural",
        "ordre": 41,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Gestionnaire en milieu rural (année 2) :
            
            - Peut expliquer le fonctionnement et le rôle des ASACO dans l'organisation des services et la prestation des soins.
            
            - Participe activement aux différents comités d'évaluation de l'exercice professionnel et aux activités de monitorage.
            
            - Contribue à l'élaboration et à l'implantation des stratégies avancées et du micro plan sanitaire.
            
            - Démontre des connaissances de base en comptabilité dans la planification des inventaires et dans les différents rapports produits pour le CSCOM.
            
            - Assurer le maintien de capital du DV.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A2-GEST",
                "ordre": 1,
                "titre": "Gestion - Gestion des données",
                "volume_horaire": 10,
                "description": "Cours sur la gestion des données et la planification en première ligne (10h).",
                "contenu": textwrap.dedent(
                    """
                    Gestion des données et planification :
                    micro-planification, comptes d'exploitation, remplissage des supports.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 31, "titre": "La micro-planification", "type": "lecon"},
                    {"numero": 32, "titre": "Comptes d'exploitation", "type": "lecon"},
                    {"numero": 33, "titre": "Remplissage des supports", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Érudit",
        "classe_code": "DES-A2",
        "titre": "Érudit – Développement professionnel continu et recherche en milieu rural",
        "ordre": 51,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Érudit en milieu rural (année 2) :
            
            - Contribue à l'éducation des patients, de la communauté et des différents membres de l'équipe de soins en partageant de manière adaptée son savoir (causeries éducatives, staff, formation des relais).
            
            - Fait preuve de curiosité scientifique et collabore activement au développement de ses compétences.
            
            - Applique de façon critique les données probantes selon le contexte de pratique et la réalité des patients et des communautés.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A2-METH",
                "ordre": 1,
                "titre": "Méthodologie de la recherche - Clubs de lecture",
                "volume_horaire": 10,
                "description": "Cours sur la méthodologie de la recherche et l'analyse critique de la littérature (10h).",
                "contenu": textwrap.dedent(
                    """
                    Développement des compétences en recherche et analyse critique :
                    analyse critique de la littérature médicale, niveaux de preuve, application
                    des données probantes au contexte de pratique.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 34, "titre": "Analyse critique de la littérature", "type": "lecon"},
                    {"numero": 35, "titre": "Niveaux de preuve", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Professionnel",
        "classe_code": "DES-A2",
        "titre": "Professionnel – Éthique et responsabilité en milieu rural",
        "ordre": 61,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Professionnel en milieu rural (année 2) :
            
            - Respecte la spécificité socioculturelle du patient et tient compte des dimensions éthiques dans son approche.
            
            - Démontre respect et honnêteté dans ses rapports professionnels.
            
            - Assure une bonne qualité et continuité de service aux patients et à la communauté en se positionnant comme médecin traitant et gestionnaire responsable.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A2-ETH",
                "ordre": 1,
                "titre": "Éthique et déontologie",
                "volume_horaire": 3,
                "description": "Cours sur l'éthique et la déontologie médicale (3h).",
                "contenu": textwrap.dedent(
                    """
                    Éthique et déontologie en pratique médicale :
                    discussion éthique, respect de la spécificité socioculturelle du patient,
                    dimensions éthiques dans l'approche clinique.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 36, "titre": "Discussion éthique", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A2-INFO",
                "ordre": 2,
                "titre": "Informatique médicale",
                "volume_horaire": 10,
                "description": "Cours sur l'informatique médicale et les outils de présentation (10h).",
                "contenu": textwrap.dedent(
                    """
                    Compétences en informatique médicale :
                    critères d'une bonne présentation, utilisation de Word, Excel, PowerPoint
                    pour la documentation et la communication médicale.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 37, "titre": "Critères d'une bonne présentation", "type": "lecon"},
                    {"numero": 38, "titre": "Word", "type": "lecon"},
                    {"numero": 39, "titre": "Excel", "type": "lecon"},
                    {"numero": 40, "titre": "PowerPoint", "type": "lecon"},
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Structure les jalons/cours/leçons UNIQUEMENT pour la DEUXIÈME ANNÉE (DES-A2) du DESMFMC. Pour les autres années, utiliser les commandes correspondantes."

    def add_arguments(self, parser):
        parser.add_argument(
            '--classe',
            default='DES-A2',
            help="Code de la classe cible - DOIT être DES-A2 pour la deuxième année (défaut: DES-A2)."
        )

    @transaction.atomic
    def handle(self, *args, **options):
        classe_code = options['classe']
        try:
            formation = Formation.objects.get(code='DESMFMC')
        except Formation.DoesNotExist as exc:
            raise CommandError("Formation DESMFMC introuvable. Veuillez exécuter les seeds du programme au préalable.") from exc

        # Vérifier que c'est bien la deuxième année
        if classe_code != 'DES-A2':
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  ATTENTION: Cette commande est conçue pour la DEUXIÈME ANNÉE (DES-A2) uniquement. '
                    f'Vous avez spécifié {classe_code}. Les jalons peuvent ne pas correspondre.'
                )
            )
        
        try:
            classe = Classe.objects.get(code=classe_code, formation=formation)
            if classe.annee != 2:
                raise CommandError(
                    f"Cette commande est réservée à la DEUXIÈME ANNÉE (année=2). "
                    f"La classe {classe_code} est en année {classe.annee}."
                )
        except Classe.DoesNotExist as exc:
            raise CommandError(f"Classe {classe_code} introuvable pour la formation DESMFMC.") from exc

        base_date = classe.date_debut or datetime.date.today()
        cours_crees = 0
        lecons_creees = 0
        jalons_crees = 0

        for jalon_data in DES2_JALONS_DATA:
            if jalon_data['classe_code'] != classe_code:
                continue

            competence = self._get_competence(jalon_data['competence'])
            jalon, created = CompetenceJalon.objects.get_or_create(
                competence=competence,
                classe=classe,
                titre=jalon_data['titre'],
                defaults={
                    'description': jalon_data['description'],
                    'ordre': jalon_data['ordre'],
                }
            )

            if created:
                jalons_crees += 1
            else:
                jalon.description = jalon_data['description']
                jalon.ordre = jalon_data['ordre']
                jalon.save()

            # Créer/mettre à jour les cours et leçons
            for course_def in jalon_data.get('courses', []):
                cours_obj, created_cours = self._upsert_course(classe, base_date, course_def)
                if created_cours:
                    cours_crees += 1
                
                # Lier le cours au jalon
                cours_obj.jalons_competence.add(jalon)

                # Créer les leçons
                for lecon_def in course_def.get('lecons', []):
                    lecon_obj, created_lecon = self._upsert_lecon(cours_obj, lecon_def)
                    if created_lecon:
                        lecons_creees += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Seed terminé pour {classe_code}:\n'
                f'  - {jalons_crees} jalons créés\n'
                f'  - {cours_crees} cours créés\n'
                f'  - {lecons_creees} leçons créées\n'
            )
        )

    def _get_competence(self, libelle_competence):
        """Récupère ou crée une compétence par son libellé"""
        competence, _ = Competence.objects.get_or_create(
            libelle=libelle_competence,
            defaults={
                'domaine': 'savoir_faire',
                'description': f'Compétence: {libelle_competence}',
                'niveau_attendu': "Maîtrise opérationnelle à l'issue du programme",
            }
        )
        return competence

    def _upsert_course(self, classe, base_date, course_def):
        """Crée ou met à jour un cours"""
        cours_obj, created = Cours.objects.get_or_create(
            code=course_def['code'],
            classe=classe,
            defaults={
                'titre': course_def['titre'],
                'description': course_def.get('description', ''),
                'contenu': course_def.get('contenu', ''),
                'volume_horaire': course_def.get('volume_horaire', 0),
                'ordre': course_def.get('ordre', 0),
                'date_debut': base_date,
                'date_fin': classe.date_fin or base_date,
                'actif': True,
            }
        )
        
        if not created:
            cours_obj.titre = course_def['titre']
            cours_obj.description = course_def.get('description', '')
            cours_obj.contenu = course_def.get('contenu', '')
            cours_obj.volume_horaire = course_def.get('volume_horaire', 0)
            cours_obj.ordre = course_def.get('ordre', 0)
            cours_obj.save()

        return cours_obj, created

    def _upsert_lecon(self, cours, lecon_def):
        """Crée ou met à jour une leçon"""
        lecon_obj, created = Lecon.objects.get_or_create(
            cours=cours,
            numero=lecon_def['numero'],
            defaults={
                'titre': lecon_def['titre'],
                'type_lecon': lecon_def.get('type', 'lecon'),
                'ordre': lecon_def['numero'],
                'actif': True,
            }
        )
        
        if not created:
            lecon_obj.titre = lecon_def['titre']
            lecon_obj.type_lecon = lecon_def.get('type', 'lecon')
            lecon_obj.ordre = lecon_def['numero']
            lecon_obj.save()

        return lecon_obj, created

