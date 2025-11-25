#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour initialiser les documents requis pour la formation Santé communautaire.

Usage :
    python scripts/initialiser_documents_requis_sante_communautaire.py
"""
import os
import sys


if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django  # noqa: E402

django.setup()

from apps.admissions.models import DocumentRequis, SANTE_COMMUNAUTAIRE_CODE  # noqa: E402


def initialiser_documents_sante_communautaire():
    """Initialise les documents requis pour la formation Santé communautaire."""

    documents = [
        {
            'nom': "Demande manuscrite adressée au Doyen de la FMOS",
            'description': "Lettre manuscrite précisant la formation en Santé Communautaire",
            'ordre': 1,
        },
        {
            'nom': "Attestation du niveau Licence (minimum requis)",
            'description': "Document attestant que le candidat possède au moins le niveau Licence",
            'ordre': 2,
        },
        {
            'nom': "Extrait d'acte de naissance",
            'description': "Copie récente de l'extrait d'acte de naissance",
            'ordre': 3,
        },
        {
            'nom': "Copie certifiée du diplôme ou équivalent",
            'description': "Copie certifiée conforme du diplôme ou de l'équivalent",
            'ordre': 4,
        },
        {
            'nom': "Attestation de prise en charge des frais de formation",
            'description': "Document attestant de la prise en charge financière de la formation",
            'ordre': 5,
        },
    ]

    print("=== Initialisation des documents requis - Santé Communautaire ===\n")

    for doc_data in documents:
        doc, cree = DocumentRequis.objects.get_or_create(
            type_formation=SANTE_COMMUNAUTAIRE_CODE,
            nom=doc_data['nom'],
            defaults={
                'description': doc_data['description'],
                'ordre': doc_data['ordre'],
                'obligatoire': True,
                'actif': True,
            }
        )

        if cree:
            print(f"[OK] Créé : {doc.nom}")
        else:
            doc.description = doc_data['description']
            doc.ordre = doc_data['ordre']
            doc.obligatoire = True
            doc.actif = True
            doc.save()
            print(f"[UPDATE] Mis à jour : {doc.nom}")

    print(f"\n[OK] {len(documents)} documents requis initialisés pour Santé Communautaire.")


if __name__ == "__main__":
    try:
        initialiser_documents_sante_communautaire()
    except Exception as exc:  # pylint: disable=broad-except
        print(f"[ERREUR] {exc}")
        import traceback
        traceback.print_exc()

