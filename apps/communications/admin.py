from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'destinataire', 'sujet', 'date_envoi', 'lu')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('expediteur__username', 'destinataire__username', 'sujet', 'contenu')
    ordering = ('-date_envoi',)
