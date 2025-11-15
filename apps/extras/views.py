from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Bienvenue dans le module des formations extras !")

from rest_framework import viewsets
from .models import FormationExtra, InscriptionExtra, CertificatExtra
from .serializers import FormationExtraSerializer, InscriptionExtraSerializer, CertificatExtraSerializer

class FormationExtraViewSet(viewsets.ModelViewSet):
    queryset = FormationExtra.objects.all()
    serializer_class = FormationExtraSerializer

class InscriptionExtraViewSet(viewsets.ModelViewSet):
    queryset = InscriptionExtra.objects.all()
    serializer_class = InscriptionExtraSerializer

class CertificatExtraViewSet(viewsets.ModelViewSet):
    queryset = CertificatExtra.objects.all()
    serializer_class = CertificatExtraSerializer
