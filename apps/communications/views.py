# apps/communications/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.db.models import Q, Count, Max
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import Message
from apps.utilisateurs.models import Utilisateur


@login_required
def messagerie_liste(request):
    """Liste des conversations (boîte de réception)"""
    utilisateur = request.user
    
    # Récupérer les conversations (messages reçus et envoyés)
    conversations = Message.objects.filter(
        Q(destinataire=utilisateur, supprime_par_destinataire=False) |
        Q(expediteur=utilisateur, supprime_par_expediteur=False)
    ).values(
        'expediteur__id', 'expediteur__username', 'expediteur__email',
        'destinataire__id', 'destinataire__username', 'destinataire__email'
    ).annotate(
        dernier_message=Max('date_envoi'),
        nb_non_lus=Count('id', filter=Q(destinataire=utilisateur, lu=False, supprime_par_destinataire=False))
    ).order_by('-dernier_message')
    
    # Créer une liste unique des conversations
    conversations_uniques = {}
    for conv in conversations:
        if conv['expediteur__id'] == utilisateur.id:
            autre_user_id = conv['destinataire__id']
            autre_username = conv['destinataire__username']
            autre_email = conv['destinataire__email']
        else:
            autre_user_id = conv['expediteur__id']
            autre_username = conv['expediteur__username']
            autre_email = conv['expediteur__email']
        
        if autre_user_id not in conversations_uniques:
            conversations_uniques[autre_user_id] = {
                'utilisateur_id': autre_user_id,
                'username': autre_username,
                'email': autre_email,
                'dernier_message': conv['dernier_message'],
                'nb_non_lus': conv['nb_non_lus']
            }
        else:
            # Mettre à jour si le message est plus récent
            if conv['dernier_message'] > conversations_uniques[autre_user_id]['dernier_message']:
                conversations_uniques[autre_user_id]['dernier_message'] = conv['dernier_message']
            conversations_uniques[autre_user_id]['nb_non_lus'] += conv['nb_non_lus']
    
    conversations_liste = list(conversations_uniques.values())
    conversations_liste.sort(key=lambda x: x['dernier_message'], reverse=True)
    
    # Pagination
    paginator = Paginator(conversations_liste, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Compter les messages non lus
    nb_messages_non_lus = Message.objects.filter(
        destinataire=utilisateur,
        lu=False,
        supprime_par_destinataire=False
    ).count()
    
    context = {
        'page_obj': page_obj,
        'nb_messages_non_lus': nb_messages_non_lus,
    }
    
    return render(request, 'communications/messagerie_liste.html', context)


@login_required
def messagerie_conversation(request, utilisateur_id):
    """Affiche la conversation avec un utilisateur spécifique"""
    utilisateur = request.user
    autre_utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)
    
    # Récupérer tous les messages de la conversation
    messages = Message.objects.filter(
        Q(expediteur=utilisateur, destinataire=autre_utilisateur, supprime_par_expediteur=False) |
        Q(expediteur=autre_utilisateur, destinataire=utilisateur, supprime_par_destinataire=False)
    ).order_by('date_envoi')
    
    # Marquer les messages reçus comme lus
    Message.objects.filter(
        destinataire=utilisateur,
        expediteur=autre_utilisateur,
        lu=False
    ).update(lu=True, date_lecture=timezone.now())
    
    # Pagination
    paginator = Paginator(messages, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'autre_utilisateur': autre_utilisateur,
        'page_obj': page_obj,
        'messages': page_obj,
    }
    
    return render(request, 'communications/messagerie_conversation.html', context)


@login_required
def messagerie_envoyer(request):
    """Envoyer un nouveau message"""
    if request.method == 'POST':
        destinataire_id = request.POST.get('destinataire_id')
        sujet = request.POST.get('sujet', '').strip()
        contenu = request.POST.get('contenu', '').strip()
        message_parent_id = request.POST.get('message_parent_id')
        
        if not destinataire_id or not contenu:
            django_messages.error(request, 'Destinataire et contenu sont requis.')
            return redirect('messagerie_liste')
        
        try:
            destinataire = Utilisateur.objects.get(id=destinataire_id)
        except Utilisateur.DoesNotExist:
            django_messages.error(request, 'Destinataire introuvable.')
            return redirect('messagerie_liste')
        
        # Créer le message
        message = Message.objects.create(
            expediteur=request.user,
            destinataire=destinataire,
            sujet=sujet or f"Message de {request.user.username}",
            contenu=contenu,
            message_parent_id=message_parent_id if message_parent_id else None
        )
        
        django_messages.success(request, f'Message envoyé à {destinataire.username}.')
        return redirect('messagerie_conversation', utilisateur_id=destinataire.id)
    
    # GET : Formulaire d'envoi
    destinataire_id = request.GET.get('destinataire_id')
    destinataire = None
    if destinataire_id:
        try:
            destinataire = Utilisateur.objects.get(id=destinataire_id)
        except Utilisateur.DoesNotExist:
            pass
    
    # Liste des utilisateurs pour le formulaire
    utilisateurs = Utilisateur.objects.filter(is_active=True).exclude(id=request.user.id)
    
    context = {
        'destinataire': destinataire,
        'utilisateurs': utilisateurs,
    }
    
    return render(request, 'communications/messagerie_envoyer.html', context)


@login_required
def messagerie_detail(request, message_id):
    """Affiche un message spécifique"""
    message = get_object_or_404(Message, id=message_id)
    
    # Vérifier que l'utilisateur peut voir ce message
    if not message.peut_etre_vu_par(request.user):
        django_messages.error(request, 'Vous n\'avez pas accès à ce message.')
        return redirect('messagerie_liste')
    
    # Marquer comme lu si c'est le destinataire
    if message.destinataire == request.user:
        message.marquer_comme_lu()
    
    context = {
        'message': message,
    }
    
    return render(request, 'communications/messagerie_detail.html', context)


@login_required
def messagerie_supprimer(request, message_id):
    """Supprime un message (soft delete)"""
    message = get_object_or_404(Message, id=message_id)
    
    if not message.peut_etre_vu_par(request.user):
        django_messages.error(request, 'Vous n\'avez pas accès à ce message.')
        return redirect('messagerie_liste')
    
    # Soft delete
    if message.expediteur == request.user:
        message.supprime_par_expediteur = True
    if message.destinataire == request.user:
        message.supprime_par_destinataire = True
    
    message.save()
    
    django_messages.success(request, 'Message supprimé.')
    return redirect('messagerie_liste')


@login_required
def messagerie_marquer_lu(request, message_id):
    """Marque un message comme lu (AJAX)"""
    message = get_object_or_404(Message, id=message_id)
    
    if message.destinataire == request.user:
        message.marquer_comme_lu()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Accès refusé'})


@login_required
def messagerie_nb_non_lus(request):
    """Retourne le nombre de messages non lus (AJAX)"""
    nb_non_lus = Message.objects.filter(
        destinataire=request.user,
        lu=False,
        supprime_par_destinataire=False
    ).count()
    
    return JsonResponse({'nb_non_lus': nb_non_lus})
