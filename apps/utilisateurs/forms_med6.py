# apps/utilisateurs/forms_med6.py
"""
Formulaires pour l'authentification des étudiants Med 6
"""
from django import forms
from django.core.exceptions import ValidationError
from .models_med6 import EtudiantMed6


class LoginMed6Form(forms.Form):
    """
    Formulaire de connexion pour les étudiants de Médecine 6
    """
    matricule = forms.CharField(
        max_length=50,
        label="Matricule",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autofocus': True,
            'placeholder': 'Votre numéro de matricule'
        })
    )
    
    nom = forms.CharField(
        max_length=100,
        label="Nom",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom'
        })
    )
    
    prenom = forms.CharField(
        max_length=100,
        label="Prénom",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre prénom'
        })
    )
    
    def clean(self):
        import re
        
        cleaned_data = super().clean()
        matricule = cleaned_data.get('matricule', '').strip()
        prenom = cleaned_data.get('prenom', '').strip()
        nom = cleaned_data.get('nom', '').strip()
        
        # Nettoyer les espaces multiples
        matricule = re.sub(r'\s+', ' ', matricule) if matricule else ""
        prenom = re.sub(r'\s+', ' ', prenom) if prenom else ""
        nom = re.sub(r'\s+', ' ', nom) if nom else ""
        
        if not matricule or not prenom or not nom:
            raise ValidationError("Veuillez remplir tous les champs (matricule, nom et prénom).")
        
        # Mettre à jour les données nettoyées
        cleaned_data['matricule'] = matricule
        cleaned_data['prenom'] = prenom
        cleaned_data['nom'] = nom
        
        # VALIDATION STRICTE: Chercher l'étudiant actif avec une liste valide
        # La méthode get_etudiant_actif vérifie déjà que le matricule, nom ET prénom correspondent
        etudiant = EtudiantMed6.get_etudiant_actif(matricule, prenom, nom)
        
        if not etudiant:
            raise ValidationError(
                "❌ Aucun étudiant de 6ème année de médecine trouvé avec ces informations dans la liste Excel active. "
                "Ce cours est réservé UNIQUEMENT aux étudiants en 6ème année de médecine.\n\n"
                "Veuillez vérifier :\n"
                "- Votre matricule (exactement comme dans la liste officielle)\n"
                "- Votre nom (exactement comme dans la liste officielle)\n"
                "- Votre prénom (exactement comme dans la liste officielle)\n\n"
                "Note: La comparaison est insensible à la casse et aux accents, mais les valeurs doivent correspondre exactement.\n\n"
                "Si vous êtes bien un étudiant de 6ème année de médecine et que vos informations sont correctes "
                "mais que vous ne pouvez pas vous connecter, contactez l'administration."
            )
        
        # Vérification supplémentaire (redondante mais sécurisée)
        if not etudiant.verifier_identite(matricule, prenom, nom):
            raise ValidationError(
                "❌ Les informations fournies ne correspondent pas exactement à celles de la liste Excel. "
                "Vérifiez votre matricule, votre nom et votre prénom."
            )
        
        # Note: On ne vérifie plus l'expiration de la liste pour permettre l'accès même si expirée
        # La vérification d'expiration est désactivée pour éviter de bloquer les étudiants
        
        # Vérifier que la liste est active
        if not etudiant.liste.active:
            raise ValidationError(
                f"❌ La liste Med 6 pour l'année {etudiant.liste.annee_universitaire} n'est plus active. "
                "Contactez l'administration."
            )
        
        cleaned_data['etudiant'] = etudiant
        return cleaned_data

