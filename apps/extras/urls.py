from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormationExtraViewSet, InscriptionExtraViewSet, CertificatExtraViewSet

router = DefaultRouter()
router.register(r'formations', FormationExtraViewSet)
router.register(r'inscriptions', InscriptionExtraViewSet)
router.register(r'certificats', CertificatExtraViewSet)

urlpatterns = [
    # path('', include(router.urls)),
]
