# apps/evaluations/forms_stage.py
"""
Formulaires pour les évaluations de stage basées sur les jalons
"""
from django import forms
from django.forms import inlineformset_factory
from .models_stage import EvaluationStage, EvaluationJalonStage
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Classe, CompetenceJalon
from apps.utilisateurs.models_programme_desmfmc import StageRotationDES, CSComUCentre


class EvaluationStageForm(forms.ModelForm):
    """Formulaire pour créer/modifier une évaluation de stage"""
    
    class Meta:
        model = EvaluationStage
        fields = [
            'etudiant', 'classe', 'stage_rotation', 'structure_stage',
            'nom_superviseur', 'type_evaluation', 'date_evaluation',
            'commentaire_general', 'signature_responsable', 'cachet_structure'
        ]
        widgets = {
            'date_evaluation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'commentaire_general': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'nom_superviseur': forms.TextInput(attrs={'class': 'form-control'}),
            'etudiant': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'stage_rotation': forms.Select(attrs={'class': 'form-control'}),
            'structure_stage': forms.Select(attrs={'class': 'form-control'}),
            'type_evaluation': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrer les étudiants selon la classe si une classe est sélectionnée
        if 'classe' in self.data:
            try:
                classe_id = int(self.data.get('classe'))
                classe = Classe.objects.get(pk=classe_id)
                self.fields['etudiant'].queryset = Utilisateur.objects.filter(
                    type_utilisateur='etudiant',
                    classe=classe.nom
                ).order_by('last_name', 'first_name')
            except (ValueError, Classe.DoesNotExist):
                pass
        
        # Filtrer les stages selon l'étudiant si un étudiant est sélectionné
        if 'etudiant' in self.data:
            try:
                etudiant_id = int(self.data.get('etudiant'))
                etudiant = Utilisateur.objects.get(pk=etudiant_id)
                self.fields['stage_rotation'].queryset = StageRotationDES.objects.filter(
                    etudiant=etudiant
                ).order_by('-annee', '-periode')
            except (ValueError, Utilisateur.DoesNotExist):
                pass
        
        # Si c'est une modification, pré-remplir les champs
        if self.instance and self.instance.pk:
            if self.instance.etudiant:
                self.fields['stage_rotation'].queryset = StageRotationDES.objects.filter(
                    etudiant=self.instance.etudiant
                ).order_by('-annee', '-periode')
            if self.instance.classe:
                self.fields['etudiant'].queryset = Utilisateur.objects.filter(
                    type_utilisateur='etudiant',
                    classe=self.instance.classe.nom
                ).order_by('last_name', 'first_name')
        
        # Définir l'enseignant automatiquement
        if user and user.est_enseignant():
            self.fields['nom_superviseur'].help_text = f"Laissez vide pour utiliser votre nom ({user.get_full_name() or user.username})"


class EvaluationJalonStageForm(forms.ModelForm):
    """Formulaire pour évaluer un jalon spécifique"""
    
    class Meta:
        model = EvaluationJalonStage
        fields = ['jalon', 'niveau', 'commentaire', 'ordre']
        widgets = {
            'jalon': forms.HiddenInput(),
            'niveau': forms.Select(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Commentaire pour cette compétence...'}),
            'ordre': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Le jalon est pré-rempli, on ne le montre pas dans le formulaire


# Formset pour les évaluations de jalons
EvaluationJalonStageFormSet = inlineformset_factory(
    EvaluationStage,
    EvaluationJalonStage,
    form=EvaluationJalonStageForm,
    extra=0,
    can_delete=False,
    min_num=1,
    validate_min=True,
)

