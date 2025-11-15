from rest_framework import serializers
from .models import FormationExtra, InscriptionExtra, CertificatExtra

class FormationExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormationExtra
        fields = '__all__'

class InscriptionExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = InscriptionExtra
        fields = '__all__'

class CertificatExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificatExtra
        fields = '__all__'
