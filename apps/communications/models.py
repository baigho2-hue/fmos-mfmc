from django.db import models
from django.urls import reverse
from apps.utilisateurs.models import Utilisateur

class Message(models.Model):
    """Modèle pour les messages internes entre utilisateurs"""
    expediteur = models.ForeignKey(
        Utilisateur, 
        on_delete=models.CASCADE, 
        related_name='messages_envoyes',
        verbose_name="Expéditeur"
    )
    destinataire = models.ForeignKey(
        Utilisateur, 
        on_delete=models.CASCADE, 
        related_name='messages_recus',
        verbose_name="Destinataire"
    )
    sujet = models.CharField(max_length=200, verbose_name="Sujet")
    contenu = models.TextField(verbose_name="Contenu")
    date_envoi = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    lu = models.BooleanField(default=False, verbose_name="Lu")
    date_lecture = models.DateTimeField(null=True, blank=True, verbose_name="Date de lecture")
    
    # Message parent pour les conversations (réponses)
    message_parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reponses',
        verbose_name="Message parent"
    )
    
    # Pièces jointes (optionnel pour l'instant)
    piece_jointe = models.FileField(
        upload_to='messages/pieces_jointes/',
        null=True,
        blank=True,
        verbose_name="Pièce jointe"
    )
    
    # Message supprimé (soft delete)
    supprime_par_expediteur = models.BooleanField(default=False)
    supprime_par_destinataire = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-date_envoi']
        indexes = [
            models.Index(fields=['destinataire', 'lu']),
            models.Index(fields=['expediteur', 'date_envoi']),
        ]
    
    def __str__(self):
        return f"{self.expediteur.username} → {self.destinataire.username} : {self.sujet}"
    
    def marquer_comme_lu(self):
        """Marque le message comme lu"""
        if not self.lu:
            from django.utils import timezone
            self.lu = True
            self.date_lecture = timezone.now()
            self.save(update_fields=['lu', 'date_lecture'])
    
    def peut_etre_vu_par(self, utilisateur):
        """Vérifie si l'utilisateur peut voir ce message"""
        return utilisateur == self.expediteur or utilisateur == self.destinataire
    
    def get_absolute_url(self):
        """URL pour voir le message"""
        return reverse('messagerie_detail', kwargs={'message_id': self.id})
