# apps/evaluations/forms_import.py
"""
Formulaires pour l'import de grilles depuis Word
"""
from django import forms
from .models_grilles import TypeGrilleEvaluation
from apps.utilisateurs.models_formation import Cours, Classe


class ImportGrilleWordForm(forms.Form):
    """Formulaire pour importer une grille depuis un document Word"""
    fichier = forms.FileField(
        label="Fichier Word (.docx)",
        help_text="Sélectionnez un fichier Word contenant la structure de la grille",
        widget=forms.FileInput(attrs={'accept': '.docx'})
    )
    type_grille = forms.ModelChoiceField(
        queryset=TypeGrilleEvaluation.objects.none(),  # Sera défini dans __init__
        label="Type de grille",
        help_text="Sélectionnez le type de grille d'évaluation"
    )
    cours = forms.ModelChoiceField(
        queryset=Cours.objects.all(),
        required=False,
        label="Cours associé",
        help_text="Optionnel : associer la grille à un cours spécifique"
    )
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        required=False,
        label="Classe associée",
        help_text="Optionnel : associer la grille à une classe spécifique"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Évaluer le queryset dynamiquement pour les types de grilles
        self.fields['type_grille'].queryset = TypeGrilleEvaluation.objects.filter(actif=True).order_by('type_grille', 'nom')
    
    def clean_fichier(self):
        fichier = self.cleaned_data.get('fichier')
        if fichier:
            if not fichier.name.endswith('.docx'):
                raise forms.ValidationError("Le fichier doit être au format .docx")
            if fichier.size > 10 * 1024 * 1024:  # 10 MB
                raise forms.ValidationError("Le fichier est trop volumineux (max 10 MB)")
        return fichier

