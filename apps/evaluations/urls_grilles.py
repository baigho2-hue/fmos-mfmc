# apps/evaluations/urls_grilles.py
"""
URLs pour les grilles d'évaluation
"""
from django.urls import path
from django.http import HttpResponse
import tempfile
import os
from .views_grilles import (
    GrilleEvaluationListView,
    GrilleEvaluationDetailView,
    EvaluationAvecGrilleCreateView,
    ImportGrilleWordView,
    export_grille_csv,
    export_evaluation_csv
)
from .importers.import_word_grille import create_word_template

app_name = 'grilles'

def download_template_view(request):
    """Vue pour télécharger le modèle Word"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
        create_word_template(tmp_file.name)
        with open(tmp_file.name, 'rb') as f:
            content = f.read()
        os.unlink(tmp_file.name)
    
    response = HttpResponse(
        content,
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename="template_grille_evaluation.docx"'
    return response

urlpatterns = [
    path('', GrilleEvaluationListView.as_view(), name='liste'),
    path('import/', ImportGrilleWordView.as_view(), name='import_word'),
    path('template/', download_template_view, name='download_template'),
    path('<int:pk>/', GrilleEvaluationDetailView.as_view(), name='detail'),
    path('<int:grille_id>/evaluer/', EvaluationAvecGrilleCreateView.as_view(), name='evaluer'),
    path('<int:grille_id>/export/', export_grille_csv, name='export_grille'),
    path('evaluation/<int:evaluation_id>/export/', export_evaluation_csv, name='export_evaluation'),
]
