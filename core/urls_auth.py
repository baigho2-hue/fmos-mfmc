# core/urls_auth.py
"""
URLs pour l'authentification
"""
from django.urls import path
from core import views, views_med6, views_2fa

urlpatterns = [
    # Authentification
    path('login/', views.login_view, name='login'),
    path('login/med6/', views_med6.login_med6, name='login_med6'),
    path('logout/', views.logout_view, name='logout'),
    
    # Double authentification (2FA)
    path('2fa/activer/', views_2fa.activer_2fa, name='activer_2fa'),
    path('2fa/verifier/', views_2fa.verifier_code_2fa_view, name='verifier_code_2fa'),
    path('2fa/desactiver/', views_2fa.desactiver_2fa, name='desactiver_2fa'),
    path('2fa/verifier-session/', views_2fa.verifier_2fa_session, name='verifier_2fa_session'),
]

