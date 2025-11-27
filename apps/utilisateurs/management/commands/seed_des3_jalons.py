"""
Commande de seed pour les jalons, cours et leçons de la TROISIÈME ANNÉE uniquement du DESMFMC.

⚠️  IMPORTANT: Cette commande est réservée à la classe DES-A3 (année 3) uniquement.
Pour les années 1, 2 et 4, utiliser les commandes correspondantes.

Source des données: Programme DESMFMC - Année 3
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


# ⚠️  DONNÉES UNIQUEMENT POUR LA TROISIÈME ANNÉE (DES-A3)
DES3_JALONS_DATA = [
    {
        "competence": "Expert médical en MF/MC",
        "classe_code": "DES-A3",
        "titre": "Expert médical – Soins spécialisés et urgences en milieu urbain (troisième année)",
        "ordre": 10,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Expert médical en milieu urbain (année 3) :
            
            - Démontre un bon niveau de connaissances théoriques et cliniques dans l'évaluation et les soins qu'il prodigue aux patients en particulier au niveau de la santé des femmes, des soins chroniques et des soins de santé mentale.
            
            - Procède à une évaluation pertinente et globale des problèmes de santé en prenant en considération les particularités culturelles et la perspective du patient.
            
            - Adapte son approche et sa conduite en tenant compte des caractéristiques du milieu et des ressources du CSCOM et des patients.
            
            - Prend les mesures nécessaires pour assurer le suivi des examens de dépistage et la continuité des soins particulièrement dans le suivi des maladies chroniques, des problèmes de santé mentale et clientèles vulnérables.
            
            - Maîtrise les différents gestes techniques à poser de façon urgente.
            
            - Mener des activités du monitorage du CSCom.
            
            - Collecter, analyser et transmettre les données du Système d'Information Sanitaire de Routine.
            
            - Organiser et réaliser une campagne de vaccination de masse.
            
            - Démontre un bon jugement clinique dans l'évaluation et le plan d'intervention et de traitement des problèmes de santé des patients.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A3-SANTE-MENTALE",
                "ordre": 1,
                "titre": "Santé mentale",
                "volume_horaire": 26,
                "description": "Cours sur la santé mentale en première ligne (26h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge des troubles mentaux en première ligne :
                    troubles anxieux, troubles dépressifs, troubles de la personnalité,
                    troubles psychotiques et délirants, troubles du sommeil, patient suicidaire,
                    psychose aiguë.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 1, "titre": "Troubles anxieux", "type": "lecon"},
                    {"numero": 2, "titre": "Troubles dépressifs", "type": "lecon"},
                    {"numero": 3, "titre": "Troubles de la personnalité", "type": "lecon"},
                    {"numero": 4, "titre": "Troubles psychotiques et délirants", "type": "lecon"},
                    {"numero": 5, "titre": "Troubles du sommeil", "type": "lecon"},
                    {"numero": 6, "titre": "Patient suicidaire", "type": "lecon"},
                    {"numero": 7, "titre": "Psychose aiguë", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-URG-OBS",
                "ordre": 2,
                "titre": "Urgences obstétricales",
                "volume_horaire": 21,
                "description": "Cours sur les urgences obstétricales niveau II (21h).",
                "contenu": textwrap.dedent(
                    """
                    Gestion des urgences obstétricales de niveau II :
                    gesta niveau II, complications obstétricales avancées.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 8, "titre": "Gesta niveau II", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-URG-MED",
                "ordre": 3,
                "titre": "Urgences Médicales",
                "volume_horaire": 30,
                "description": "Cours sur les urgences médicales en première ligne (30h).",
                "contenu": textwrap.dedent(
                    """
                    Gestion des urgences médicales :
                    infections aiguës, traumatismes mineurs, gestion de la douleur aiguë,
                    syndrome coronarien aigu, dyspnée aiguë, convulsions, urgences ophtalmiques et ORL,
                    urgences pédiatriques, problèmes locomoteurs aigus, problèmes bucco-dentaires,
                    état de mal épileptique.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 9, "titre": "Infections aiguës", "type": "lecon"},
                    {"numero": 10, "titre": "Traumatismes mineurs", "type": "lecon"},
                    {"numero": 11, "titre": "Gestion de la douleur aiguë", "type": "lecon"},
                    {"numero": 12, "titre": "Syndrome Coronarien aigu", "type": "lecon"},
                    {"numero": 13, "titre": "Dyspnée aiguë", "type": "lecon"},
                    {"numero": 14, "titre": "Convulsions", "type": "lecon"},
                    {"numero": 15, "titre": "Urgences ophtalmiques et ORL", "type": "lecon"},
                    {"numero": 16, "titre": "Urgences pédiatriques", "type": "lecon"},
                    {"numero": 17, "titre": "Problèmes locomoteurs aigus", "type": "lecon"},
                    {"numero": 18, "titre": "Problèmes bucco-dentaires", "type": "lecon"},
                    {"numero": 19, "titre": "État de mal épileptique", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-MED-FREQ",
                "ordre": 4,
                "titre": "Médecine - Problèmes fréquents chez l'adulte et l'adolescent",
                "volume_horaire": 20,
                "description": "Cours sur les problèmes de santé fréquents chez l'adulte et l'adolescent (20h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge des problèmes de santé fréquents :
                    asthme, problèmes cutanés (acné, eczéma, psoriasis, gale, teigne),
                    céphalées, vertiges et étourdissements, problèmes digestifs hauts et bas,
                    problèmes locomoteurs, infections sexuellement transmissibles,
                    arthrose/arthrite, maladies infectieuses.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 20, "titre": "Asthme", "type": "lecon"},
                    {"numero": 21, "titre": "Problèmes cutanés (acné, eczéma, psoriasis, gale, teigne)", "type": "lecon"},
                    {"numero": 22, "titre": "Céphalées", "type": "lecon"},
                    {"numero": 23, "titre": "Vertiges et étourdissements", "type": "lecon"},
                    {"numero": 24, "titre": "Problèmes digestifs hauts et bas", "type": "lecon"},
                    {"numero": 25, "titre": "Problèmes locomoteurs", "type": "lecon"},
                    {"numero": 26, "titre": "Infections Sexuellement transmissibles", "type": "lecon"},
                    {"numero": 27, "titre": "Arthrose/Arthrite", "type": "lecon"},
                    {"numero": 28, "titre": "Maladies infectieuses", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-MED-CHRON",
                "ordre": 5,
                "titre": "Médecine - Suivi des maladies chroniques",
                "volume_horaire": 20,
                "description": "Cours sur le suivi des maladies chroniques en première ligne (20h).",
                "contenu": textwrap.dedent(
                    """
                    Suivi et prise en charge des maladies chroniques :
                    HTA, maladie vasculaire athérosclérotique, insuffisance cardiaque,
                    BPCO, diabète, SIDA, cancer, tuberculose, épilepsie.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 29, "titre": "HTA", "type": "lecon"},
                    {"numero": 30, "titre": "Maladie vasculaire athérosclérotique", "type": "lecon"},
                    {"numero": 31, "titre": "Insuffisance cardiaque", "type": "lecon"},
                    {"numero": 32, "titre": "BPCO", "type": "lecon"},
                    {"numero": 33, "titre": "Diabète", "type": "lecon"},
                    {"numero": 34, "titre": "SIDA", "type": "lecon"},
                    {"numero": 35, "titre": "Cancer", "type": "lecon"},
                    {"numero": 36, "titre": "Tuberculose", "type": "lecon"},
                    {"numero": 37, "titre": "Épilepsie", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-GERIATRIE",
                "ordre": 6,
                "titre": "Gériatrie",
                "volume_horaire": 24,
                "description": "Cours sur la gériatrie et la prise en charge des personnes âgées (24h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge gériatrique :
                    vieillissement normal et pathologique, démences, délirium et troubles du comportement,
                    troubles de la marche et chutes, incontinences et rétention,
                    problèmes cutanés courants, pharmacothérapie chez la personne âgée.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 38, "titre": "Vieillissement normale", "type": "lecon"},
                    {"numero": 39, "titre": "Vieillissement pathologique", "type": "lecon"},
                    {"numero": 40, "titre": "Les démences, délirium et trouble du comportement", "type": "lecon"},
                    {"numero": 41, "titre": "Troubles de la marche et chutes", "type": "lecon"},
                    {"numero": 42, "titre": "Incontinences et rétention", "type": "lecon"},
                    {"numero": 43, "titre": "Problèmes cutanés courants", "type": "lecon"},
                    {"numero": 44, "titre": "Pharmacothérapie chez la personne âgée", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Communicateur",
        "classe_code": "DES-A3",
        "titre": "Communicateur – Communication avancée en contexte complexe en milieu urbain",
        "ordre": 20,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Communicateur en milieu urbain (année 3) :
            
            - Démontre des habiletés relationnelles et de communication dans des contextes de soins complexes (mauvaise nouvelle, problèmes de santé mentale, problèmes de violence, différends).
            
            - Transmet clairement et dans un langage adapté les informations médicales et les recommandations aux patients et à leur famille pour favoriser l'adhésion et la conformité aux traitements.
            
            - Produit les documents médicaux de façon claire et pertinente pour le suivi ou le transfert des patients.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A3-COMM-BEHAV",
                "ordre": 1,
                "titre": "Communication et sciences comportementales",
                "volume_horaire": 21,
                "description": "Cours sur la communication avancée et les sciences comportementales (21h).",
                "contenu": textwrap.dedent(
                    """
                    Communication thérapeutique avancée et sciences comportementales :
                    approche des troubles psychiques ou psycho-comportementales (anxiété, dépression, trouble de la personnalité),
                    annonce d'une mauvaise nouvelle, niveaux de soins,
                    approches des victimes de violences (femmes, enfants, personnes âgées).
                    """
                ).strip(),
                "lecons": [
                    {"numero": 45, "titre": "Approche des troubles psychiques ou psycho-comportementales (anxiété, dépression, trouble de la personnalité)", "type": "lecon"},
                    {"numero": 46, "titre": "Annonce d'une mauvaise nouvelle", "type": "lecon"},
                    {"numero": 47, "titre": "Niveaux de Soins", "type": "lecon"},
                    {"numero": 48, "titre": "Approches des victimes de violences (femmes, enfants, personnes âgées)", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Collaborateur",
        "classe_code": "DES-A3",
        "titre": "Collaborateur – Collaboration interprofessionnelle avancée en milieu urbain",
        "ordre": 22,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Collaborateur en milieu urbain (année 3) :
            
            - Prend l'initiative de solliciter l'opinion des différents collaborateurs en fonction de leur expertise et de leur apport aux soins des patients.
            
            - Réfère de façon pertinente et judicieuse aux différentes ressources professionnelles et communautaires (professionnels de la santé, relais, ASACO) pour optimiser la qualité des soins et services aux patients et à la population.
            
            - Communique et explique les informations médicales pertinentes dans un langage adapté aux différents acteurs et membres de l'équipe de soins justifiant la nécessité de leur contribution.
            """
        ).strip(),
        "courses": [],
    },
    {
        "competence": "Promoteur de la santé",
        "classe_code": "DES-A3",
        "titre": "Promoteur de la santé – Promotion et prévention avancées en milieu urbain",
        "ordre": 31,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Promoteur de la santé en milieu urbain (année 3) :
            
            - Planifie, organise et anime les séances de vaccination, rencontres de formation avec les relais, causeries éducatives et les campagnes promotionnelles des CPN.
            
            - Conseille et mobilise de manière efficace les patients et la population aux activités de dépistage et de guidance en lien avec les programmes nationaux de santé publique (malnutrition, infections respiratoires, maladies diarrhéiques, paludisme, VIH-SIDA, IST, planification familiale, etc.).
            
            - Identifie et analyse les facteurs de risque et de récidive de certaines pathologies lors des consultations et des visites de milieu avec les relais.
            
            - Propose des activités intégrées pour optimiser l'impact des recommandations de santé.
            """
        ).strip(),
        "courses": [],
    },
    {
        "competence": "Gestionnaire",
        "classe_code": "DES-A3",
        "titre": "Gestionnaire – Gestion avancée des services en milieu urbain",
        "ordre": 41,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Gestionnaire en milieu urbain (année 3) :
            
            - Participe activement au comité de gestion du CSCOM.
            
            - Mobilise les membres de l'ASACO quant à l'organisation des services et des soins pour favoriser la santé de leur communauté.
            
            - Monitore les données et produit un rapport des activités visant la qualité des services du CSCOM (inventaire des stocks, rapport financier, atteinte des cibles des programmes nationaux).
            
            - Propose des mesures correctrices et des stratégies avancées pour répondre aux besoins sanitaires de sa communauté.
            
            - Planifie et organise des activités d'évaluation de l'exercice professionnel.
            """
        ).strip(),
        "courses": [],
    },
    {
        "competence": "Érudit",
        "classe_code": "DES-A3",
        "titre": "Érudit – Recherche et développement professionnel continu en milieu urbain",
        "ordre": 30,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Érudit en milieu urbain (année 3) :
            
            - Contribue à l'éducation des patients et de la communauté de même qu'à la formation du personnel dans un langage adapté (causeries éducatives, staff, formation des relais).
            
            - Fait preuve de curiosité scientifique et collabore activement au développement de ses compétences.
            
            - Applique de façon critique les données probantes selon le contexte de pratique et la réalité des patients et des communautés.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A3-ERUD-CLUB",
                "ordre": 1,
                "titre": "Érudition - Clubs de lecture",
                "volume_horaire": 10,
                "description": "Cours sur l'érudition et les clubs de lecture (10h).",
                "contenu": textwrap.dedent(
                    """
                    Développement de l'érudition médicale :
                    participation aux clubs de lecture, analyse critique de la littérature,
                    partage des connaissances avec les pairs.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 49, "titre": "Clubs de lecture", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-METH-RECH",
                "ordre": 2,
                "titre": "Méthodologie de la recherche",
                "volume_horaire": 10,
                "description": "Cours sur la méthodologie de la recherche médicale (10h).",
                "contenu": textwrap.dedent(
                    """
                    Méthodologie de la recherche en médecine de première ligne :
                    plan d'un protocole de recherche, conception d'études,
                    application des méthodes de recherche au contexte de pratique.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 50, "titre": "Plan d'un protocole de recherche", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Professionnel",
        "classe_code": "DES-A3",
        "titre": "Professionnel – Éthique et responsabilité en milieu urbain",
        "ordre": 40,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Professionnel en milieu urbain (année 3) :
            
            - Respecte la spécificité socioculturelle du patient et tient compte des dimensions éthiques dans son approche.
            
            - Démontre respect et honnêteté dans ses rapports professionnels.
            
            - Se positionne comme médecin traitant et gestionnaire responsable.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A3-ETH",
                "ordre": 1,
                "titre": "Éthique et déontologie",
                "volume_horaire": 6,
                "description": "Cours sur l'éthique et la déontologie médicale avancées (6h).",
                "contenu": textwrap.dedent(
                    """
                    Éthique et déontologie médicale avancées :
                    discussion éthique, dilemmes éthiques en pratique médicale,
                    application des principes éthiques dans des situations complexes.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 51, "titre": "Discussion éthique", "type": "lecon"},
                ],
            },
        ],
    },
    # ===================================================================
    # JALONS POUR LE MILIEU RURAL (même classe DES-A3, jalons différents)
    # ===================================================================
    {
        "competence": "Expert médical en MF/MC",
        "classe_code": "DES-A3",
        "titre": "Expert médical – Soins spécialisés et urgences en milieu rural (troisième année)",
        "ordre": 11,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Expert médical en milieu rural (année 3) :
            
            - Démontre un bon niveau de connaissances théoriques et cliniques dans l'évaluation et les soins qu'il prodigue aux patients en particulier au niveau de la santé des femmes, des soins chroniques et des soins de santé mentale.
            
            - Procède à une évaluation pertinente et globale des problèmes de santé en prenant en considération les particularités culturelles et la perspective du patient.
            
            - Adapte son approche et sa conduite en tenant compte des caractéristiques du milieu et des ressources du CSCOM et des patients.
            
            - Prend les mesures nécessaires pour assurer le suivi des examens de dépistage et la continuité des soins particulièrement dans le suivi des maladies chroniques, des problèmes de santé mentale et clientèles vulnérables.
            
            - Maîtrise les différents gestes techniques à poser de façon urgente.
            
            - Démontre un bon jugement clinique dans l'évaluation et le plan d'intervention et de traitement des problèmes de santé des patients.
            
            - Assurer un accouchement dystocique.
            
            - Pratiquer une épisiotomie et épisioraphie.
            
            - Assurer la PEC de la MAM et MAS.
            """
        ).strip(),
        "courses": [
            # Réutilisation des mêmes cours que le milieu urbain (get_or_create les réutilisera)
            {
                "code": "DES-A3-SANTE-MENTALE",
                "ordre": 1,
                "titre": "Santé mentale",
                "volume_horaire": 26,
                "description": "Cours sur la santé mentale en première ligne (26h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge des troubles mentaux en première ligne :
                    troubles anxieux, troubles dépressifs, troubles de la personnalité,
                    troubles psychotiques et délirants, troubles du sommeil, patient suicidaire,
                    psychose aiguë.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 1, "titre": "Troubles anxieux", "type": "lecon"},
                    {"numero": 2, "titre": "Troubles dépressifs", "type": "lecon"},
                    {"numero": 3, "titre": "Troubles de la personnalité", "type": "lecon"},
                    {"numero": 4, "titre": "Troubles psychotiques et délirants", "type": "lecon"},
                    {"numero": 5, "titre": "Troubles du sommeil", "type": "lecon"},
                    {"numero": 6, "titre": "Patient suicidaire", "type": "lecon"},
                    {"numero": 7, "titre": "Psychose aiguë", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-URG-OBS",
                "ordre": 2,
                "titre": "Urgences obstétricales",
                "volume_horaire": 21,
                "description": "Cours sur les urgences obstétricales niveau II (21h).",
                "contenu": textwrap.dedent(
                    """
                    Gestion des urgences obstétricales de niveau II :
                    gesta niveau II, complications obstétricales avancées.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 8, "titre": "Gesta niveau II", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-URG-MED",
                "ordre": 3,
                "titre": "Urgences Médicales",
                "volume_horaire": 30,
                "description": "Cours sur les urgences médicales en première ligne (30h).",
                "contenu": textwrap.dedent(
                    """
                    Gestion des urgences médicales :
                    infections aiguës, traumatismes mineurs, gestion de la douleur aiguë,
                    syndrome coronarien aigu, dyspnée aiguë, convulsions, urgences ophtalmiques et ORL,
                    urgences pédiatriques, problèmes locomoteurs aigus, problèmes bucco-dentaires,
                    état de mal épileptique.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 9, "titre": "Infections aiguës", "type": "lecon"},
                    {"numero": 10, "titre": "Traumatismes mineurs", "type": "lecon"},
                    {"numero": 11, "titre": "Gestion de la douleur aiguë", "type": "lecon"},
                    {"numero": 12, "titre": "Syndrome Coronarien aigu", "type": "lecon"},
                    {"numero": 13, "titre": "Dyspnée aiguë", "type": "lecon"},
                    {"numero": 14, "titre": "Convulsions", "type": "lecon"},
                    {"numero": 15, "titre": "Urgences ophtalmiques et ORL", "type": "lecon"},
                    {"numero": 16, "titre": "Urgences pédiatriques", "type": "lecon"},
                    {"numero": 17, "titre": "Problèmes locomoteurs aigus", "type": "lecon"},
                    {"numero": 18, "titre": "Problèmes bucco-dentaires", "type": "lecon"},
                    {"numero": 19, "titre": "État de mal épileptique", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-MED-FREQ",
                "ordre": 4,
                "titre": "Médecine - Problèmes fréquents chez l'adulte et l'adolescent",
                "volume_horaire": 20,
                "description": "Cours sur les problèmes de santé fréquents chez l'adulte et l'adolescent (20h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge des problèmes de santé fréquents :
                    asthme, problèmes cutanés (acné, eczéma, psoriasis, gale, teigne),
                    céphalées, vertiges et étourdissements, problèmes digestifs hauts et bas,
                    problèmes locomoteurs, infections sexuellement transmissibles,
                    arthrose/arthrite, maladies infectieuses.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 20, "titre": "Asthme", "type": "lecon"},
                    {"numero": 21, "titre": "Problèmes cutanés (acné, eczéma, psoriasis, gale, teigne)", "type": "lecon"},
                    {"numero": 22, "titre": "Céphalées", "type": "lecon"},
                    {"numero": 23, "titre": "Vertiges et étourdissements", "type": "lecon"},
                    {"numero": 24, "titre": "Problèmes digestifs hauts et bas", "type": "lecon"},
                    {"numero": 25, "titre": "Problèmes locomoteurs", "type": "lecon"},
                    {"numero": 26, "titre": "Infections Sexuellement transmissibles", "type": "lecon"},
                    {"numero": 27, "titre": "Arthrose/Arthrite", "type": "lecon"},
                    {"numero": 28, "titre": "Maladies infectieuses", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-DERM",
                "ordre": 5,
                "titre": "Dermatologie",
                "volume_horaire": 18,
                "description": "Cours sur la dermatologie avancée en première ligne (18h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge dermatologique avancée :
                    dermatoses infectieuses complexes, dermatoses auto-immunes,
                    dermatoses allergiques, pathologies cutanées systémiques,
                    dermatologie pédiatrique, dermatologie gériatrique.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 29, "titre": "Dermatoses infectieuses complexes", "type": "lecon"},
                    {"numero": 30, "titre": "Dermatoses auto-immunes", "type": "lecon"},
                    {"numero": 31, "titre": "Dermatoses allergiques et urticaires", "type": "lecon"},
                    {"numero": 32, "titre": "Pathologies cutanées systémiques", "type": "lecon"},
                    {"numero": 33, "titre": "Dermatologie pédiatrique", "type": "lecon"},
                    {"numero": 34, "titre": "Dermatologie gériatrique", "type": "lecon"},
                    {"numero": 35, "titre": "Dermatoses liées aux médicaments", "type": "lecon"},
                    {"numero": 36, "titre": "Prise en charge des ulcères chroniques", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-MED-CHRON",
                "ordre": 6,
                "titre": "Médecine - Suivi des maladies chroniques",
                "volume_horaire": 20,
                "description": "Cours sur le suivi des maladies chroniques en première ligne (20h).",
                "contenu": textwrap.dedent(
                    """
                    Suivi et prise en charge des maladies chroniques :
                    HTA, maladie vasculaire athérosclérotique, insuffisance cardiaque,
                    BPCO, diabète, SIDA, cancer, tuberculose, épilepsie.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 37, "titre": "HTA", "type": "lecon"},
                    {"numero": 38, "titre": "Maladie vasculaire athérosclérotique", "type": "lecon"},
                    {"numero": 39, "titre": "Insuffisance cardiaque", "type": "lecon"},
                    {"numero": 40, "titre": "BPCO", "type": "lecon"},
                    {"numero": 41, "titre": "Diabète", "type": "lecon"},
                    {"numero": 42, "titre": "SIDA", "type": "lecon"},
                    {"numero": 43, "titre": "Cancer", "type": "lecon"},
                    {"numero": 44, "titre": "Tuberculose", "type": "lecon"},
                    {"numero": 45, "titre": "Épilepsie", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-GERIATRIE",
                "ordre": 7,
                "titre": "Gériatrie",
                "volume_horaire": 24,
                "description": "Cours sur la gériatrie et la prise en charge des personnes âgées (24h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge gériatrique :
                    vieillissement normal et pathologique, démences, délirium et troubles du comportement,
                    troubles de la marche et chutes, incontinences et rétention,
                    problèmes cutanés courants, pharmacothérapie chez la personne âgée.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 46, "titre": "Vieillissement normale", "type": "lecon"},
                    {"numero": 47, "titre": "Vieillissement pathologique", "type": "lecon"},
                    {"numero": 48, "titre": "Les démences, délirium et trouble du comportement", "type": "lecon"},
                    {"numero": 49, "titre": "Troubles de la marche et chutes", "type": "lecon"},
                    {"numero": 50, "titre": "Incontinences et rétention", "type": "lecon"},
                    {"numero": 51, "titre": "Problèmes cutanés courants", "type": "lecon"},
                    {"numero": 52, "titre": "Pharmacothérapie chez la personne âgée", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Communicateur",
        "classe_code": "DES-A3",
        "titre": "Communicateur – Communication avancée en contexte complexe en milieu rural",
        "ordre": 21,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Communicateur en milieu rural (année 3) :
            
            - Démontre des habiletés relationnelles et de communication dans des contextes de soins complexes (mauvaise nouvelle, problèmes de santé mentale, problèmes de violence, différends).
            
            - Transmet clairement et dans un langage adapté les informations médicales et les recommandations aux patients et à leur famille pour favoriser l'adhésion et la conformité aux traitements.
            
            - Produit les documents médicaux de façon claire et pertinente pour le suivi ou le transfert des patients.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A3-COMM-BEHAV",
                "ordre": 1,
                "titre": "Communication et sciences comportementales",
                "volume_horaire": 21,
                "description": "Cours sur la communication avancée et les sciences comportementales (21h).",
                "contenu": textwrap.dedent(
                    """
                    Communication thérapeutique avancée et sciences comportementales :
                    approche des troubles psychiques ou psycho-comportementales (anxiété, dépression, trouble de la personnalité),
                    annonce d'une mauvaise nouvelle, niveaux de soins,
                    approches des victimes de violences (femmes, enfants, personnes âgées).
                    """
                ).strip(),
                "lecons": [
                    {"numero": 45, "titre": "Approche des troubles psychiques ou psycho-comportementales (anxiété, dépression, trouble de la personnalité)", "type": "lecon"},
                    {"numero": 46, "titre": "Annonce d'une mauvaise nouvelle", "type": "lecon"},
                    {"numero": 47, "titre": "Niveaux de Soins", "type": "lecon"},
                    {"numero": 48, "titre": "Approches des victimes de violences (femmes, enfants, personnes âgées)", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Collaborateur",
        "classe_code": "DES-A3",
        "titre": "Collaborateur – Collaboration interprofessionnelle avancée en milieu rural",
        "ordre": 22,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Collaborateur en milieu rural (année 3) :
            
            - Prend l'initiative de solliciter l'opinion des différents collaborateurs en fonction de leur expertise et de leur apport aux soins des patients.
            
            - Réfère de façon pertinente et judicieuse aux différentes ressources professionnelles et communautaires (professionnels de la santé, relais, ASACO) pour optimiser la qualité des soins et services aux patients et à la population.
            
            - Communique et explique les informations médicales pertinentes dans un langage adapté aux différents acteurs et membres de l'équipe de soins justifiant la nécessité de leur contribution.
            """
        ).strip(),
        "courses": [],
    },
    {
        "competence": "Promoteur de la santé",
        "classe_code": "DES-A3",
        "titre": "Promoteur de la santé – Promotion et prévention avancées en milieu rural",
        "ordre": 31,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Promoteur de la santé en milieu rural (année 3) :
            
            - Planifie, organise et anime les séances de vaccination, rencontres de formation avec les relais, causeries éducatives et les campagnes promotionnelles des CPN.
            
            - Conseille et mobilise de manière efficace les patients et la population aux activités de dépistage et de guidance en lien avec les programmes nationaux de santé publique (malnutrition, infections respiratoires, maladies diarrhéiques, paludisme, VIH-SIDA, IST, planification familiale, etc.).
            
            - Identifie et analyse les facteurs de risque et de récidive de certaines pathologies lors des consultations et des visites de milieu avec les relais.
            
            - Propose des activités intégrées pour optimiser l'impact des recommandations de santé.
            """
        ).strip(),
        "courses": [],
    },
    {
        "competence": "Gestionnaire",
        "classe_code": "DES-A3",
        "titre": "Gestionnaire – Gestion avancée des services en milieu rural",
        "ordre": 41,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Gestionnaire en milieu rural (année 3) :
            
            - Participe activement au comité de gestion du CSCOM.
            
            - Mobilise les membres de l'ASACO quant à l'organisation des services et des soins pour favoriser la santé de leur communauté.
            
            - Monitore les données et produit un rapport des activités visant la qualité des services du CSCOM (inventaire des stocks, rapport financier, atteinte des cibles des programmes nationaux).
            
            - Propose des mesures correctrices et des stratégies avancées pour répondre aux besoins sanitaires de sa communauté.
            
            - Planifie et organise des activités d'évaluation de l'exercice professionnel.
            """
        ).strip(),
        "courses": [],
    },
    {
        "competence": "Érudit",
        "classe_code": "DES-A3",
        "titre": "Érudit – Recherche et développement professionnel continu en milieu rural",
        "ordre": 51,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Érudit en milieu rural (année 3) :
            
            - Contribue à l'éducation des patients et de la communauté de même qu'à la formation du personnel dans un langage adapté (causeries éducatives, staff, formation des relais).
            
            - Fait preuve de curiosité scientifique et collabore activement au développement de ses compétences.
            
            - Applique de façon critique les données probantes selon le contexte de pratique et la réalité des patients et des communautés.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A3-ERUD-CLUB",
                "ordre": 1,
                "titre": "Érudition - Clubs de lecture",
                "volume_horaire": 10,
                "description": "Cours sur l'érudition et les clubs de lecture (10h).",
                "contenu": textwrap.dedent(
                    """
                    Développement de l'érudition médicale :
                    participation aux clubs de lecture, analyse critique de la littérature,
                    partage des connaissances avec les pairs.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 49, "titre": "Clubs de lecture", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A3-METH-RECH",
                "ordre": 2,
                "titre": "Méthodologie de la recherche",
                "volume_horaire": 10,
                "description": "Cours sur la méthodologie de la recherche médicale (10h).",
                "contenu": textwrap.dedent(
                    """
                    Méthodologie de la recherche en médecine de première ligne :
                    plan d'un protocole de recherche, conception d'études,
                    application des méthodes de recherche au contexte de pratique.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 50, "titre": "Plan d'un protocole de recherche", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Professionnel",
        "classe_code": "DES-A3",
        "titre": "Professionnel – Éthique et responsabilité en milieu rural",
        "ordre": 61,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Professionnel en milieu rural (année 3) :
            
            - Respecte la spécificité socioculturelle du patient et tient compte des dimensions éthiques dans son approche.
            
            - Démontre respect et honnêteté dans ses rapports professionnels.
            
            - Se positionne comme médecin traitant et gestionnaire responsable.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A3-ETH",
                "ordre": 1,
                "titre": "Éthique et déontologie",
                "volume_horaire": 6,
                "description": "Cours sur l'éthique et la déontologie médicale avancées (6h).",
                "contenu": textwrap.dedent(
                    """
                    Éthique et déontologie médicale avancées :
                    discussion éthique, dilemmes éthiques en pratique médicale,
                    application des principes éthiques dans des situations complexes.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 51, "titre": "Discussion éthique", "type": "lecon"},
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Structure les jalons/cours/leçons UNIQUEMENT pour la TROISIÈME ANNÉE (DES-A3) du DESMFMC. Pour les autres années, utiliser les commandes correspondantes."

    def add_arguments(self, parser):
        parser.add_argument(
            '--classe',
            default='DES-A3',
            help="Code de la classe cible - DOIT être DES-A3 pour la troisième année (défaut: DES-A3)."
        )

    @transaction.atomic
    def handle(self, *args, **options):
        classe_code = options['classe']
        try:
            formation = Formation.objects.get(code='DESMFMC')
        except Formation.DoesNotExist as exc:
            raise CommandError("Formation DESMFMC introuvable. Veuillez exécuter les seeds du programme au préalable.") from exc

        # Vérifier que c'est bien la troisième année
        if classe_code != 'DES-A3':
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  ATTENTION: Cette commande est conçue pour la TROISIÈME ANNÉE (DES-A3) uniquement. '
                    f'Vous avez spécifié {classe_code}. Les jalons peuvent ne pas correspondre.'
                )
            )
        
        try:
            classe = Classe.objects.get(code=classe_code, formation=formation)
            if classe.annee != 3:
                raise CommandError(
                    f"Cette commande est réservée à la TROISIÈME ANNÉE (année=3). "
                    f"La classe {classe_code} est en année {classe.annee}."
                )
        except Classe.DoesNotExist as exc:
            raise CommandError(f"Classe {classe_code} introuvable pour la formation DESMFMC.") from exc

        base_date = classe.date_debut or datetime.date.today()
        cours_crees = 0
        lecons_creees = 0
        jalons_crees = 0

        for jalon_data in DES3_JALONS_DATA:
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

