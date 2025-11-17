from django.urls import path
from . import views

urlpatterns = [
    path('', views.messagerie_liste, name='messagerie_liste'),
    path('envoyer/', views.messagerie_envoyer, name='messagerie_envoyer'),
    path('conversation/<int:utilisateur_id>/', views.messagerie_conversation, name='messagerie_conversation'),
    path('message/<int:message_id>/', views.messagerie_detail, name='messagerie_detail'),
    path('message/<int:message_id>/supprimer/', views.messagerie_supprimer, name='messagerie_supprimer'),
    path('message/<int:message_id>/marquer-lu/', views.messagerie_marquer_lu, name='messagerie_marquer_lu'),
    path('api/nb-non-lus/', views.messagerie_nb_non_lus, name='messagerie_nb_non_lus'),
]
