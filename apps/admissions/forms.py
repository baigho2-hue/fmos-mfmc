"""
Formulaires pour les admissions et inscriptions
"""
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, password_validation

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

    first_name = forms.CharField(label="Prénom", max_length=150, required=False)
    last_name = forms.CharField(label="Nom", max_length=150, required=False)
    email = forms.EmailField(label="Email", required=False)
    telephone = forms.CharField(label="Téléphone", max_length=30, required=False)
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        required=False,
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = DossierCandidature
        fields = ['formation', 'prise_en_charge_bourse', 'details_bourse']
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

        self.requires_account = not (self.request_user and self.request_user.is_authenticated)
        extra_fields = ['first_name', 'last_name', 'email', 'telephone', 'password1', 'password2']
        if self.requires_account:
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['email'].required = True
            self.fields['password1'].required = True
            self.fields['password2'].required = True
        else:
            for field in extra_fields:
                self.fields[field].widget = forms.HiddenInput()
                self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        if self.requires_account:
            email = cleaned_data.get('email')
            password1 = cleaned_data.get('password1')
            password2 = cleaned_data.get('password2')

            if not email:
                self.add_error('email', "L'email est requis.")
            else:
                UserModel = get_user_model()
                if UserModel.objects.filter(email__iexact=email).exists():
                    self.add_error('email', "Cet email est déjà utilisé.")

            if password1 and password2:
                if password1 != password2:
                    self.add_error('password2', "Les mots de passe ne correspondent pas.")
                else:
                    try:
                        password_validation.validate_password(password1)
                    except ValidationError as exc:
                        self.add_error('password1', exc)
            else:
                if not password1:
                    self.add_error('password1', "Mot de passe requis.")
                if not password2:
                    self.add_error('password2', "Veuillez confirmer le mot de passe.")

        return cleaned_data


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

