from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'destinataire', 'sujet', 'date_envoi', 'lu', 'date_lecture')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('expediteur__username', 'destinataire__username', 'sujet', 'contenu')
    ordering = ('-date_envoi',)
    readonly_fields = ('date_envoi', 'date_lecture')
    fieldsets = (
        ('Message', {
            'fields': ('expediteur', 'destinataire', 'sujet', 'contenu', 'message_parent')
        }),
        ('Statut', {
            'fields': ('lu', 'date_envoi', 'date_lecture')
        }),
        ('Fichiers', {
            'fields': ('piece_jointe',)
        }),
        ('Suppression', {
            'fields': ('supprime_par_expediteur', 'supprime_par_destinataire'),
            'classes': ('collapse',)
        }),
    )
