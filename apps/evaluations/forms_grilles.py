# apps/evaluations/forms_grilles.py
"""
Formulaires pour les grilles d'évaluation
"""
from django import forms
from django.forms import inlineformset_factory
from .models_grilles import (
    GrilleEvaluation,
    CritereEvaluation,
    ElementEvaluation,
    EvaluationAvecGrille,
    ReponseCritere,
    ReponseElement,
    TypeGrilleEvaluation
)
from apps.utilisateurs.models_formation import Cours, Classe, Competence, CompetenceJalon


class TypeGrilleEvaluationForm(forms.ModelForm):
    """Formulaire pour créer/modifier un type de grille"""
    class Meta:
        model = TypeGrilleEvaluation
        fields = ['code', 'nom', 'description', 'type_grille', 'actif']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class GrilleEvaluationForm(forms.ModelForm):
    """Formulaire pour créer/modifier une grille d'évaluation"""
    class Meta:
        model = GrilleEvaluation
        fields = [
            'type_grille', 'titre', 'description', 'cours', 'classe',
            'competences_evaluees', 'jalons_evalues', 'note_maximale',
            'echelle_evaluation', 'actif'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'competences_evaluees': forms.SelectMultiple(attrs={'size': 10}),
            'jalons_evalues': forms.SelectMultiple(attrs={'size': 10}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les compétences et jalons si un cours/classe est sélectionné
        if 'cours' in self.data:
            try:
                cours_id = int(self.data.get('cours'))
                cours = Cours.objects.get(pk=cours_id)
                if cours.classe:
                    self.fields['jalons_evalues'].queryset = CompetenceJalon.objects.filter(
                        classe=cours.classe
                    )
            except (ValueError, Cours.DoesNotExist):
                pass


class CritereEvaluationForm(forms.ModelForm):
    """Formulaire pour créer/modifier un critère d'évaluation"""
    class Meta:
        model = CritereEvaluation
        fields = [
            'ordre', 'libelle', 'description', 'poids', 'note_maximale',
            'competence', 'jalon', 'actif'
        ]
        widgets = {
            'libelle': forms.TextInput(attrs={'size': 80}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }


class ElementEvaluationForm(forms.ModelForm):
    """Formulaire pour créer/modifier un élément d'évaluation"""
    class Meta:
        model = ElementEvaluation
        fields = ['ordre', 'libelle', 'description', 'poids', 'actif']
        widgets = {
            'libelle': forms.TextInput(attrs={'size': 80}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }


# Formset pour les critères
CritereFormSet = inlineformset_factory(
    GrilleEvaluation,
    CritereEvaluation,
    form=CritereEvaluationForm,
    extra=1,
    can_delete=True,
    can_order=True,
)

# Formset pour les éléments d'un critère
ElementFormSet = inlineformset_factory(
    CritereEvaluation,
    ElementEvaluation,
    form=ElementEvaluationForm,
    extra=1,
    can_delete=True,
    can_order=True,
)


class EvaluationAvecGrilleForm(forms.ModelForm):
    """Formulaire pour créer une évaluation avec une grille"""
    class Meta:
        model = EvaluationAvecGrille
        fields = [
            'grille', 'etudiant', 'evaluateur', 'note_obtenue', 'note_sur',
            'commentaires_generaux', 'points_forts', 'axes_amelioration',
            'date_evaluation'
        ]
        widgets = {
            'date_evaluation': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'commentaires_generaux': forms.Textarea(attrs={'rows': 4}),
            'points_forts': forms.Textarea(attrs={'rows': 3}),
            'axes_amelioration': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        grille_id = kwargs.pop('grille_id', None)
        super().__init__(*args, **kwargs)
        if grille_id:
            self.fields['grille'].initial = grille_id
            self.fields['grille'].widget = forms.HiddenInput()


class ReponseCritereForm(forms.ModelForm):
    """Formulaire pour évaluer un critère"""
    class Meta:
        model = ReponseCritere
        fields = ['critere', 'note', 'niveau', 'commentaire']
        widgets = {
            'critere': forms.HiddenInput(),
            'commentaire': forms.Textarea(attrs={'rows': 2}),
        }


class ReponseElementForm(forms.ModelForm):
    """Formulaire pour évaluer un élément"""
    class Meta:
        model = ReponseElement
        fields = ['element', 'note', 'niveau', 'commentaire']
        widgets = {
            'element': forms.HiddenInput(),
            'commentaire': forms.Textarea(attrs={'rows': 2}),
        }

