from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Utilisateur
from .models_formation import PaiementCours

class InscriptionEtudiantForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre.email@example.com'})
    )
    email_confirmation = forms.EmailField(
        required=True,
        label="Confirmer l'adresse e-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre email'})
    )
    first_name = forms.CharField(
        required=True,
        max_length=150,
        label="Prénom",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=True,
        max_length=150,
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    classe = forms.CharField(
        required=True,
        max_length=50,
        label="Classe",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Médecine 6, DESMFMC 1ère année'}),
        help_text="Indiquez votre classe ou niveau de formation"
    )
    
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'email_confirmation', 'first_name', 'last_name', 'classe', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Vérifier si l'email existe déjà
            if Utilisateur.objects.filter(email=email).exists():
                # Si on est en train de modifier un utilisateur existant, on peut ignorer son propre email
                if self.instance and self.instance.pk:
                    existing_user = Utilisateur.objects.get(email=email)
                    if existing_user.pk == self.instance.pk:
                        return email
                raise ValidationError("Cette adresse e-mail est déjà utilisée. Veuillez utiliser une autre adresse ou vous connecter.")
        return email
    
    def clean_email_confirmation(self):
        email = self.cleaned_data.get('email')
        email_confirmation = self.cleaned_data.get('email_confirmation')
        if email and email_confirmation and email != email_confirmation:
            raise ValidationError("Les adresses e-mail ne correspondent pas.")
        return email_confirmation
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.type_utilisateur = 'etudiant'
        user.email = self.cleaned_data['email']
        user.email_verifie = False  # À vérifier par email
        if commit:
            user.save()
        return user

class InscriptionEnseignantForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre.email@example.com'})
    )
    email_confirmation = forms.EmailField(
        required=True,
        label="Confirmer l'adresse e-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre email'})
    )
    first_name = forms.CharField(
        required=True,
        max_length=150,
        label="Prénom",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=True,
        max_length=150,
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    matieres = forms.CharField(
        required=True,
        max_length=500,
        label="Matières enseignées",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Médecine de famille, Santé communautaire, Recherche'}),
        help_text="Liste des matières que vous enseignez, séparées par des virgules"
    )
    
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'email_confirmation', 'first_name', 'last_name', 'matieres', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Vérifier si l'email existe déjà
            if Utilisateur.objects.filter(email=email).exists():
                # Si on est en train de modifier un utilisateur existant, on peut ignorer son propre email
                if self.instance and self.instance.pk:
                    existing_user = Utilisateur.objects.get(email=email)
                    if existing_user.pk == self.instance.pk:
                        return email
                raise ValidationError("Cette adresse e-mail est déjà utilisée. Veuillez utiliser une autre adresse ou vous connecter.")
        return email
    
    def clean_email_confirmation(self):
        email = self.cleaned_data.get('email')
        email_confirmation = self.cleaned_data.get('email_confirmation')
        if email and email_confirmation and email != email_confirmation:
            raise ValidationError("Les adresses e-mail ne correspondent pas.")
        return email_confirmation
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.type_utilisateur = 'enseignant'
        user.email = self.cleaned_data['email']
        user.email_verifie = False  # À vérifier par email
        user.niveau_acces = 'standard'  # Par défaut, peut être modifié par admin
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur ou Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'placeholder': 'Entrez votre nom d\'utilisateur ou email'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Essayer de trouver l'utilisateur par username ou email
            try:
                user = Utilisateur.objects.get(username=username)
            except Utilisateur.DoesNotExist:
                try:
                    user = Utilisateur.objects.get(email=username)
                except Utilisateur.DoesNotExist:
                    raise ValidationError({
                        'username': "Nom d'utilisateur ou email incorrect."
                    })
            
            # Vérifier le mot de passe
            if not user.check_password(password):
                raise ValidationError({
                    'password': "Mot de passe incorrect."
                })
            
            # Vérifier que le compte est actif
            if not user.is_active:
                raise ValidationError("Ce compte est désactivé.")
            
            self.user_cache = user
        else:
            raise ValidationError("Veuillez remplir tous les champs.")
        
        return self.cleaned_data


class CodeVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        label="Code de vérification",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez le code à 6 chiffres',
            'autofocus': True,
            'maxlength': '6',
            'pattern': '[0-9]{6}'
        }),
        help_text="Entrez le code à 6 chiffres envoyé à votre adresse email"
    )


class PaiementCoursForm(forms.ModelForm):
    """Formulaire pour créer un paiement de cours"""
    
    class Meta:
        model = PaiementCours
        fields = ['cours', 'montant', 'mode_paiement', 'reference_paiement', 'preuve_paiement', 'commentaires']
        widgets = {
            'cours': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
            'reference_paiement': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de transaction, référence, etc.'
            }),
            'preuve_paiement': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf'
            }),
            'commentaires': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Informations complémentaires (optionnel)'
            }),
        }
        labels = {
            'cours': 'Cours',
            'montant': 'Montant (FCFA)',
            'mode_paiement': 'Mode de paiement',
            'reference_paiement': 'Référence de paiement',
            'preuve_paiement': 'Preuve de paiement',
            'commentaires': 'Commentaires',
        }
        help_texts = {
            'reference_paiement': 'Numéro de transaction, référence Orange Money, numéro de virement, etc.',
            'preuve_paiement': 'Capture d\'écran, reçu de paiement, etc. (formats acceptés: images, PDF)',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Limiter les cours aux cours accessibles par l'étudiant
        if user and user.type_utilisateur == 'etudiant':
            from .models_formation import Cours
            from core.views_med6 import a_acces_gratuit_med6
            
            # Récupérer les cours de la classe de l'étudiant
            classe_obj = user.get_classe_obj()
            if classe_obj:
                queryset = Cours.objects.filter(
                    classe=classe_obj,
                    actif=True
                )
                
                # Si l'étudiant a accès gratuit Med6, exclure les cours Med6 (gratuits)
                if a_acces_gratuit_med6(user):
                    # Exclure les cours de la classe Med6 (gratuits pour cet étudiant)
                    queryset = queryset.exclude(classe__nom__icontains='Médecine 6')
                
                self.fields['cours'].queryset = queryset.order_by('titre')
            else:
                self.fields['cours'].queryset = Cours.objects.none()
        elif user and user.type_utilisateur != 'etudiant':
            # Pour les admins/enseignants, afficher tous les cours
            from .models_formation import Cours
            self.fields['cours'].queryset = Cours.objects.filter(actif=True).order_by('titre')