# apps/extras/admin.py
from django.contrib import admin
from .models import CertificatExtra, FormationExtra, InscriptionExtra, ModuleExtra

# -------------------------
# Certificat Extra
# -------------------------
# @admin.register(CertificatExtra)
class CertificatExtraAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'titre', 'date_obtention')
    list_filter = ('date_obtention',)
    search_fields = ('etudiant__username', 'titre')
    ordering = ('date_obtention',)

# -------------------------
# Formation Extra
# -------------------------
#
class FormationExtraAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('nom',)
    ordering = ('date_creation',)

# -------------------------
# Inscription Extra
# -------------------------
# @admin.register(InscriptionExtra)
class InscriptionExtraAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'formation_extra', 'date_inscription')
    list_filter = ('formation_extra', 'date_inscription')
    search_fields = ('etudiant__username', 'formation_extra__nom')
    ordering = ('date_inscription',)

# -------------------------
# Module Extra
# -------------------------
from django.contrib import admin
from .models import FormationExtra, InscriptionExtra, ModuleExtra, PaiementExtra, CertificatExtra

# @admin.register(FormationExtra)
class FormationExtraAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_formation', 'tarification', 'prix', 'date_debut', 'date_fin', 'actif')
    list_filter = ('type_formation', 'tarification', 'actif')
    search_fields = ('titre', 'description')
    ordering = ('date_debut',)

# @admin.register(InscriptionExtra)
class InscriptionExtraAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'formation', 'date_inscription', 'valide')
    list_filter = ('valide', 'formation')
    search_fields = ('utilisateur__username', 'formation__titre')
    ordering = ('-date_inscription',)

# @admin.register(ModuleExtra)
class ModuleExtraAdmin(admin.ModelAdmin):
    list_display = ('titre', 'formation_extra')
    list_filter = ('formation_extra',)
    search_fields = ('titre', 'description')
    ordering = ('formation_extra', 'titre')

# @admin.register(PaiementExtra)
class PaiementExtraAdmin(admin.ModelAdmin):
    list_display = ('inscription_extra', 'montant', 'mode_paiement', 'reference_paiement', 'date_paiement', 'valide')
    list_filter = ('valide', 'mode_paiement')
    search_fields = ('inscription_extra__utilisateur__username', 'reference_paiement')
    ordering = ('-date_paiement',)
    readonly_fields = ('date_paiement',)

# @admin.register(CertificatExtra)
class CertificatExtraAdmin(admin.ModelAdmin):
    list_display = ('inscription', 'code_certificat', 'date_emission')
    search_fields = ('inscription__utilisateur__username', 'code_certificat')
    ordering = ('-date_emission',)
