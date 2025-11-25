"""
Formulaires pour les admissions et inscriptions
"""
from django import forms
from django.core.exceptions import ValidationError

from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Formation
from .models import (
    DossierCandidature,
    DocumentDossier,
    DocumentRequis,
    Inscription,
)


class DossierCandidatureForm(forms.ModelForm):
    """Formulaire pour créer un dossier de candidature."""

    first_name = forms.CharField(label="Prénom", max_length=150, required=True)
    last_name = forms.CharField(label="Nom", max_length=150, required=True)
    email = forms.EmailField(label="Email", required=True)
    telephone = forms.CharField(label="Téléphone", max_length=30, required=False)

    class Meta:
        model = DossierCandidature
        fields = [
            'formation',
            'prise_en_charge_bourse',
            'details_bourse',
            'last_name',
            'first_name',
            'email',
            'telephone',
        ]
        widgets = {
            'formation': forms.Select(attrs={'class': 'form-control'}),
            'prise_en_charge_bourse': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'details_bourse': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Préciser les détails de la bourse si applicable'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.candidat = kwargs.pop('candidat', None)
        self.request_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['formation'].queryset = Formation.objects.filter(actif=True)
        self.fields['formation'].empty_label = "Sélectionner une formation"
        self.fields['details_bourse'].required = False

        if self.request_user and self.request_user.is_authenticated:
            self.fields['first_name'].initial = self.request_user.first_name
            self.fields['last_name'].initial = self.request_user.last_name
            self.fields['email'].initial = self.request_user.email
            self.fields['telephone'].initial = getattr(self.request_user, 'telephone', '')
            for field in ('first_name', 'last_name', 'email', 'telephone'):
                self.fields[field].required = False
                self.fields[field].widget = forms.HiddenInput()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.prenom_candidat = self.cleaned_data.get('first_name')
        instance.nom_candidat = self.cleaned_data.get('last_name')
        instance.email_contact = self.cleaned_data.get('email')
        instance.telephone_contact = self.cleaned_data.get('telephone')
        if self.request_user and self.request_user.is_authenticated:
            instance.candidat = self.request_user
        if commit:
            instance.save()
        return instance


class DocumentUploadForm(forms.ModelForm):
    """Formulaire pour uploader un document requis."""
    
    class Meta:
        model = DocumentDossier
        fields = ['document_requis', 'fichier']
        widgets = {
            'document_requis': forms.HiddenInput(),
            'fichier': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.dossier = kwargs.pop('dossier', None)
        self.document_requis = kwargs.pop('document_requis', None)
        super().__init__(*args, **kwargs)
        
        if self.document_requis:
            self.fields['document_requis'].initial = self.document_requis
            self.fields['document_requis'].widget = forms.HiddenInput()
    
    def clean_fichier(self):
        fichier = self.cleaned_data.get('fichier')
        if not fichier:
            raise ValidationError("Veuillez sélectionner un fichier.")
        
        # Vérifier la taille (max 10MB)
        if fichier.size > 10 * 1024 * 1024:
            raise ValidationError("Le fichier est trop volumineux (maximum 10MB).")
        
        # Vérifier l'extension
        extensions_autorisees = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png']
        nom_fichier = fichier.name.lower()
        if not any(nom_fichier.endswith(ext) for ext in extensions_autorisees):
            raise ValidationError(
                f"Format de fichier non autorisé. Formats acceptés: {', '.join(extensions_autorisees)}"
            )
        
        return fichier
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.dossier:
            instance.dossier = self.dossier
        if commit:
            instance.save()
        return instance


class InscriptionForm(forms.ModelForm):
    """Formulaire pour l'inscription administrative."""
    
    class Meta:
        model = Inscription
        fields = ['commentaires_validation']
        widgets = {
            'commentaires_validation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Commentaires optionnels'
            }),
        }


class InscriptionPaiementForm(forms.ModelForm):
    """Formulaire pour le paiement de l'inscription (formations certifiantes uniquement)."""
    
    class Meta:
        model = Inscription
        fields = ['mode_paiement', 'reference_paiement', 'preuve_paiement']
        widgets = {
            'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
            'reference_paiement': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de transaction, référence Orange Money, etc.'
            }),
            'preuve_paiement': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
        }
    
    def clean_preuve_paiement(self):
        preuve = self.cleaned_data.get('preuve_paiement')
        if preuve:
            # Vérifier la taille (max 5MB)
            if preuve.size > 5 * 1024 * 1024:
                raise ValidationError("Le fichier est trop volumineux (maximum 5MB).")
            
            # Vérifier l'extension
            extensions_autorisees = ['.pdf', '.jpg', '.jpeg', '.png']
            nom_fichier = preuve.name.lower()
            if not any(nom_fichier.endswith(ext) for ext in extensions_autorisees):
                raise ValidationError(
                    f"Format de fichier non autorisé. Formats acceptés: {', '.join(extensions_autorisees)}"
                )
        
        return preuve


class DossierCompletForm(forms.Form):
    """Formulaire pour vérifier la complétude d'un dossier."""
    
    def __init__(self, *args, **kwargs):
        self.dossier = kwargs.pop('dossier', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        if self.dossier:
            if not self.dossier.verifier_completude():
                documents_manquants = self.dossier.get_documents_manquants()
                if documents_manquants:
                    noms_manquants = ', '.join([doc.nom for doc in documents_manquants])
                    raise ValidationError(
                        f"Le dossier est incomplet. Documents manquants ou non validés: {noms_manquants}"
                    )
        return cleaned_data

