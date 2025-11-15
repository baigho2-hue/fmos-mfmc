from django.contrib import admin
from .models import Activite

@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'responsable', 'echeance', 'realisee')
    list_filter = ('realisee', 'responsable')
    search_fields = ('titre', 'responsable__username')
    ordering = ('echeance',)
