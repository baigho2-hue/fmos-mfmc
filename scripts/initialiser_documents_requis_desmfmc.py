#!/usr/bin/env python
"""
Script pour initialiser les documents requis pour le dossier DESMFMC.

Usage :
    python scripts/initialiser_documents_requis_desmfmc.py
"""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django  # noqa: E402

django.setup()

from apps.admissions.models import DocumentRequis  # noqa: E402


def initialiser_documents_desmfmc():
    """Initialise les 6 documents requis pour le dossier DESMFMC."""
    
    documents = [
        {
            'nom': 'Demande timbrée adressée au doyen de la FMOS',
            'description': 'Une demande timbrée adressée au doyen de la FMOS (une copie)',
            'ordre': 1,
        },
        {
            'nom': 'Diplôme de doctorat en médecine générale',
            'description': 'Une copie du diplôme de doctorat (ou attestation) en médecine générale plus la lettre d\'équivalence pour les diplômes étrangers',
            'ordre': 2,
        },
        {
            'nom': 'Autorisation d\'inscription de la fonction publique',
            'description': 'Une autorisation d\'inscription de la fonction publique pour les fonctionnaires d\'État',
            'ordre': 3,
        },
        {
            'nom': 'Extrait d\'acte de naissance',
            'description': 'Un extrait d\'acte de naissance ou du jugement supplétif',
            'ordre': 4,
        },
        {
            'nom': 'Certificat d\'engagement de prise en charge des frais de formation',
            'description': 'Un certificat d\'engagement de prise en charge des frais de formation',
            'ordre': 5,
        },
        {
            'nom': 'Préciser si études prises en charge par une bourse',
            'description': 'Préciser si les études sont prises en charge par une bourse',
            'ordre': 6,
        },
    ]
    
    print("=== Initialisation des documents requis pour DESMFMC ===\n")
    
    for doc_data in documents:
        doc, cree = DocumentRequis.objects.get_or_create(
            type_formation='DESMFMC',
            nom=doc_data['nom'],
            defaults={
                'description': doc_data['description'],
                'ordre': doc_data['ordre'],
                'obligatoire': True,
                'actif': True,
            }
        )
        
        if cree:
            print(f"✅ Créé: {doc.nom}")
        else:
            # Mettre à jour si nécessaire
            doc.description = doc_data['description']
            doc.ordre = doc_data['ordre']
            doc.obligatoire = True
            doc.actif = True
            doc.save()
            print(f"🔄 Mis à jour: {doc.nom}")
    
    print(f"\n✅ {len(documents)} documents requis initialisés pour DESMFMC.")


if __name__ == "__main__":
    try:
        initialiser_documents_desmfmc()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

