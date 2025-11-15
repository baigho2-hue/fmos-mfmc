from django import forms
from .models import FormationExtra, InscriptionExtra, PaiementExtra


class InscriptionMultiFormationForm(forms.Form):
    """Formulaire pour l'inscription à plusieurs formations avec calcul du coût total"""
    
    MODE_PAIEMENT_CHOICES = [
        ('espece', 'Espèces'),
        ('bancaire', 'Virement bancaire'),
        ('orange_money', 'Orange Money'),
    ]
    
    formations = forms.ModelMultipleChoiceField(
        queryset=FormationExtra.objects.filter(actif=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'formation-checkbox'}),
        label="Sélectionnez les formations",
        required=True,
        help_text="Vous pouvez sélectionner une ou plusieurs formations"
    )
    
    mode_paiement = forms.ChoiceField(
        choices=MODE_PAIEMENT_CHOICES,
        label="Mode de paiement",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        help_text="Le mode de paiement sera demandé après validation de votre inscription par l'administration"
    )
    
    reference_paiement = forms.CharField(
        max_length=100,
        label="Référence du paiement (optionnel)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Numéro de transaction, référence virement, etc.'
        }),
        help_text="Si vous avez déjà effectué un paiement, indiquez la référence"
    )
    
    confirmation = forms.BooleanField(
        label="Je confirme mon inscription et j'accepte que ma demande soit soumise à validation par l'administration",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Trier les formations par titre
        self.fields['formations'].queryset = FormationExtra.objects.filter(actif=True).order_by('titre')


class InscriptionFormationForm(forms.Form):
    """Formulaire pour l'inscription à une formation avec paiement (ancien système)"""
    
    MODE_PAIEMENT_CHOICES = [
        ('espece', 'Espèces'),
        ('bancaire', 'Virement bancaire'),
        ('orange_money', 'Orange Money'),
    ]
    
    mode_paiement = forms.ChoiceField(
        choices=MODE_PAIEMENT_CHOICES,
        label="Mode de paiement",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    reference_paiement = forms.CharField(
        max_length=100,
        label="Référence du paiement",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Numéro de transaction, référence virement, etc. (optionnel)'
        }),
        help_text="Si vous avez déjà effectué le paiement, indiquez la référence"
    )
    
    confirmation = forms.BooleanField(
        label="Je confirme mon inscription et j'accepte les conditions",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        est_payante = kwargs.pop('est_payante', False)
        super().__init__(*args, **kwargs)
        
        if est_payante:
            self.fields['mode_paiement'].required = True
        else:
            self.fields['mode_paiement'].required = False

