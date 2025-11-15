# apps/utilisateurs/forms_carnet_stage.py
"""
Formulaires pour le carnet de stage du DESMFMC
"""
from django import forms
from django.core.exceptions import ValidationError
from .models_carnet_stage import (
    CarnetStage, EvaluationStage, EvaluationCompetence,
    TableauEvaluationClasse, EvaluationCompetenceTableau
)
from .models_programme_desmfmc import StagePremiereAnnee, StageRotationDES, JalonProgramme
from .models_formation import Competence, Classe


class CarnetStageForm(forms.ModelForm):
    """Formulaire pour créer/modifier un carnet de stage"""
    
    class Meta:
        model = CarnetStage
        fields = ['annee_scolaire', 'actif']
        widgets = {
            'annee_scolaire': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2024-2025'
            }),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'annee_scolaire': 'Année scolaire',
            'actif': 'Carnet actif'
        }


class EvaluationStageForm(forms.ModelForm):
    """Formulaire pour créer/modifier une évaluation de stage"""
    
    class Meta:
        model = EvaluationStage
        fields = [
            'annee', 'type_stage', 'stage_annee1', 'stage_rotation',
            'lieu_stage', 'service_stage', 'date_debut', 'date_fin', 'duree_semaines',
            'maitre_stage', 'maitre_stage_nom', 'maitre_stage_titre',
            'note_globale', 'appreciation_globale', 'points_forts', 'points_amelioration',
            'valide', 'date_validation', 'valide_par'
        ]
        widgets = {
            'annee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 4
            }),
            'type_stage': forms.Select(attrs={'class': 'form-control'}),
            'stage_annee1': forms.Select(attrs={'class': 'form-control'}),
            'stage_rotation': forms.Select(attrs={'class': 'form-control'}),
            'lieu_stage': forms.TextInput(attrs={'class': 'form-control'}),
            'service_stage': forms.TextInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'date_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'duree_semaines': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'maitre_stage': forms.Select(attrs={'class': 'form-control'}),
            'maitre_stage_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'maitre_stage_titre': forms.TextInput(attrs={'class': 'form-control'}),
            'note_globale': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'max': 20
            }),
            'appreciation_globale': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'points_forts': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'points_amelioration': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'valide': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_validation': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'valide_par': forms.Select(attrs={'class': 'form-control'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin and date_fin < date_debut:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")
        
        return cleaned_data


class EvaluationCompetenceForm(forms.ModelForm):
    """Formulaire pour évaluer une compétence lors d'un stage"""
    
    class Meta:
        model = EvaluationCompetence
        fields = [
            'competence', 'jalon', 'niveau_acquisition',
            'commentaire', 'observations', 'evalue_par_maitre', 'date_evaluation'
        ]
        widgets = {
            'competence': forms.Select(attrs={'class': 'form-control'}),
            'jalon': forms.Select(attrs={'class': 'form-control'}),
            'niveau_acquisition': forms.Select(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'observations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'evalue_par_maitre': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_evaluation': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }


class TableauEvaluationClasseForm(forms.ModelForm):
    """Formulaire pour créer un tableau d'évaluation par classe"""
    
    class Meta:
        model = TableauEvaluationClasse
        fields = ['classe', 'jalon', 'annee', 'competences']
        widgets = {
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'jalon': forms.Select(attrs={'class': 'form-control'}),
            'annee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 4
            }),
            'competences': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 10
            })
        }


class EvaluationCompetenceTableauForm(forms.ModelForm):
    """Formulaire pour évaluer une compétence dans un tableau"""
    
    class Meta:
        model = EvaluationCompetenceTableau
        fields = ['competence', 'niveau_acquisition', 'commentaire', 'date_evaluation']
        widgets = {
            'competence': forms.Select(attrs={'class': 'form-control'}),
            'niveau_acquisition': forms.Select(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'date_evaluation': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }


class EvaluationCompetenceInlineFormSet(forms.BaseInlineFormSet):
    """Formset pour gérer plusieurs évaluations de compétences"""
    
    def clean(self):
        if any(self.errors):
            return
        
        competences = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                competence = form.cleaned_data.get('competence')
                if competence:
                    if competence in competences:
                        raise ValidationError("Chaque compétence ne peut être évaluée qu'une seule fois.")
                    competences.append(competence)

