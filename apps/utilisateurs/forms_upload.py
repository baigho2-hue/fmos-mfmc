# apps/utilisateurs/forms_upload.py
"""
Formulaires pour l'upload de cours et leçons
"""
from django import forms
from .models_formation import Cours, Lecon, Classe, MethodePedagogique


class UploadCoursForm(forms.Form):
    """Formulaire pour téléverser un fichier de cours"""
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.filter(actif=True),
        required=True,
        label="Classe",
        help_text="Sélectionnez la classe pour ce cours"
    )
    titre = forms.CharField(
        max_length=200,
        required=True,
        label="Titre du cours",
        help_text="Titre du cours"
    )
    code = forms.CharField(
        max_length=50,
        required=True,
        label="Code du cours",
        help_text="Code unique du cours"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Description",
        help_text="Description brève du cours"
    )
    fichier_cours = forms.FileField(
        required=True,
        label="Fichier du cours",
        help_text="Fichier PDF, Word ou autre document du cours",
        widget=forms.FileInput(attrs={'accept': '.pdf,.doc,.docx,.ppt,.pptx,.txt'})
    )
    enseignant = forms.ModelChoiceField(
        queryset=None,  # Sera rempli dans la vue
        required=False,
        label="Enseignant principal",
        help_text="Enseignant responsable de ce cours"
    )
    ordre = forms.IntegerField(
        required=False,
        initial=0,
        label="Ordre d'affichage",
        help_text="Ordre dans la liste des cours (0 = premier)"
    )
    date_debut = forms.DateField(
        required=False,
        label="Date de début",
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Date de début du cours"
    )
    date_fin = forms.DateField(
        required=False,
        label="Date de fin",
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Date de fin du cours"
    )
    methodes_pedagogiques = forms.ModelMultipleChoiceField(
        queryset=MethodePedagogique.objects.all(),
        required=False,
        label="Méthodes pédagogiques",
        help_text="Vous pouvez sélectionner plusieurs méthodes pédagogiques (double, triple, etc.)",
        widget=forms.SelectMultiple(attrs={'size': '5', 'class': 'form-control'})
    )
    description_methodes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Description des méthodes",
        help_text="Décrivez comment ces méthodes sont appliquées dans ce cours"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les enseignants actifs
        from apps.utilisateurs.models import Utilisateur
        self.fields['enseignant'].queryset = Utilisateur.objects.filter(
            type_utilisateur='enseignant',
            is_active=True
        ).order_by('last_name', 'first_name')


class UploadLeconForm(forms.Form):
    """Formulaire pour téléverser un fichier de leçon"""
    cours = forms.ModelChoiceField(
        queryset=Cours.objects.filter(actif=True),
        required=True,
        label="Cours",
        help_text="Sélectionnez le cours pour cette leçon"
    )
    titre = forms.CharField(
        max_length=200,
        required=True,
        label="Titre de la leçon",
        help_text="Titre de la leçon"
    )
    numero = forms.IntegerField(
        required=False,
        initial=1,
        label="Numéro de la leçon",
        help_text="Numéro de la leçon dans le cours"
    )
    type_lecon = forms.ChoiceField(
        choices=Lecon.TYPE_LECON_CHOICES,
        initial='lecon',
        label="Type de leçon",
        help_text="Type de leçon"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Description",
        help_text="Description de la leçon"
    )
    fichier_lecon = forms.FileField(
        required=True,
        label="Fichier de la leçon",
        help_text="Fichier PDF, Word ou autre document de la leçon",
        widget=forms.FileInput(attrs={'accept': '.pdf,.doc,.docx,.ppt,.pptx,.txt,.zip'})
    )
    ordre = forms.IntegerField(
        required=False,
        initial=0,
        label="Ordre d'affichage",
        help_text="Ordre dans la liste des leçons (0 = première)"
    )
    duree_estimee = forms.IntegerField(
        required=False,
        initial=0,
        label="Durée estimée (minutes)",
        help_text="Durée estimée pour compléter cette leçon"
    )
    date_dispensation = forms.DateTimeField(
        required=False,
        label="Date de dispensation",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="Date et heure prévues pour dispenser cette leçon"
    )

