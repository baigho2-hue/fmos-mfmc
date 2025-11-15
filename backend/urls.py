from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
  

    # Apps FMOS-MFMC
    path('utilisateurs/', include('apps.utilisateurs.urls')),
    path('admissions/', include('apps.admissions.urls')),
    path('evaluations/', include('apps.evaluations.urls')),
    path('procedurier/', include('apps.procedurier.urls')),
    path('communications/', include('apps.communications.urls')),
    path('extras/', include('apps.extras.urls')), 
]