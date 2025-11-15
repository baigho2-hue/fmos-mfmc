from django.db import models
from apps.utilisateurs.models import Utilisateur

class Activite(models.Model):
    titre = models.CharField(max_length=200)
    responsable = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    echeance = models.DateField()
    realisee = models.BooleanField(default=False)
