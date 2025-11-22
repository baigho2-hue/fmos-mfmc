# core/views_paiements.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from apps.utilisateurs.models_formation import PaiementCours, Cours
from apps.utilisateurs.forms import PaiementCoursForm


@login_required(login_url='login')
def mes_paiements(request):
    """Vue pour afficher la liste des paiements de l'étudiant"""
    user = request.user
    from core.views_med6 import a_acces_gratuit_med6
    
    # Vérifier que l'utilisateur est un étudiant
    if user.type_utilisateur != 'etudiant':
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard_etudiant')
    
    # Récupérer tous les paiements de l'étudiant
    paiements = PaiementCours.objects.filter(etudiant=user).order_by('-date_paiement')
    
    # Statistiques
    total_paiements = paiements.count()
    paiements_valides = paiements.filter(statut='valide').count()
    paiements_en_attente = paiements.filter(statut='en_attente').count()
    montant_total = sum(p.montant for p in paiements.filter(statut='valide'))
    
    # Vérifier si l'étudiant a accès gratuit Med6
    acces_gratuit_med6 = a_acces_gratuit_med6(user)
    
    context = {
        'paiements': paiements,
        'total_paiements': total_paiements,
        'paiements_valides': paiements_valides,
        'paiements_en_attente': paiements_en_attente,
        'montant_total': montant_total,
        'acces_gratuit_med6': acces_gratuit_med6,
    }
    
    return render(request, 'etudiant/paiements/mes_paiements.html', context)


@login_required(login_url='login')
def creer_paiement(request):
    """Vue pour créer un nouveau paiement"""
    user = request.user
    from core.views_med6 import a_acces_gratuit_med6
    
    # Vérifier que l'utilisateur est un étudiant
    if user.type_utilisateur != 'etudiant':
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard_etudiant')
    
    # Vérifier si l'étudiant essaie de payer pour un cours Med6 alors qu'il a accès gratuit
    if request.method == 'POST' and 'cours' in request.POST:
        try:
            cours_id = request.POST.get('cours')
            if cours_id:
                cours = Cours.objects.get(id=cours_id)
                # Vérifier si c'est un cours Med6 et si l'étudiant a accès gratuit
                if cours.classe and 'Médecine 6' in cours.classe.nom and a_acces_gratuit_med6(user):
                    messages.info(
                        request,
                        f"Le cours '{cours.titre}' est gratuit pour vous car vous êtes dans la liste active des étudiants de Médecine 6. "
                        "Aucun paiement n'est nécessaire."
                    )
                    return redirect('mes_paiements')
        except Cours.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = PaiementCoursForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            cours = form.cleaned_data['cours']
            # Double vérification : si c'est un cours Med6 et que l'étudiant a accès gratuit
            if cours.classe and 'Médecine 6' in cours.classe.nom and a_acces_gratuit_med6(user):
                messages.info(
                    request,
                    f"Le cours '{cours.titre}' est gratuit pour vous car vous êtes dans la liste active des étudiants de Médecine 6. "
                    "Aucun paiement n'est nécessaire."
                )
                return redirect('mes_paiements')
            
            paiement = form.save(commit=False)
            paiement.etudiant = user
            paiement.statut = 'en_attente'
            paiement.save()
            messages.success(
                request,
                f"Votre paiement de {paiement.montant} FCFA pour le cours '{paiement.cours.titre}' a été enregistré. "
                "Il sera validé par l'administration sous peu."
            )
            return redirect('mes_paiements')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = PaiementCoursForm(user=user)
    
    # Récupérer les cours disponibles pour l'étudiant
    cours_disponibles = []
    classe_obj = user.get_classe_obj()
    if classe_obj:
        queryset = Cours.objects.filter(
            classe=classe_obj,
            actif=True
        )
        
        # Si l'étudiant a accès gratuit Med6, exclure les cours Med6
        if a_acces_gratuit_med6(user):
            queryset = queryset.exclude(classe__nom__icontains='Médecine 6')
        
        cours_disponibles = queryset.order_by('titre')
    
    # Vérifier si l'étudiant a accès gratuit Med6
    acces_gratuit_med6 = a_acces_gratuit_med6(user)
    
    context = {
        'form': form,
        'cours_disponibles': cours_disponibles,
        'acces_gratuit_med6': acces_gratuit_med6,
    }
    
    return render(request, 'etudiant/paiements/creer_paiement.html', context)


@login_required(login_url='login')
def detail_paiement(request, paiement_id):
    """Vue pour afficher les détails d'un paiement"""
    user = request.user
    
    paiement = get_object_or_404(PaiementCours, id=paiement_id)
    
    # Vérifier que l'utilisateur a le droit de voir ce paiement
    if user.type_utilisateur == 'etudiant' and paiement.etudiant != user:
        messages.error(request, "Vous n'avez pas accès à ce paiement.")
        return redirect('mes_paiements')
    
    # Vérifier si l'utilisateur est admin ou enseignant
    if user.type_utilisateur not in ['etudiant', 'enseignant', 'coordination', 'admin']:
        messages.error(request, "Accès non autorisé.")
        return redirect('index')
    
    context = {
        'paiement': paiement,
        'peut_valider': user.type_utilisateur in ['enseignant', 'coordination', 'admin'],
    }
    
    return render(request, 'etudiant/paiements/detail_paiement.html', context)


@login_required(login_url='login')
def valider_paiement(request, paiement_id):
    """Vue pour valider un paiement (admin/enseignant/coordination uniquement)"""
    user = request.user
    
    # Vérifier les permissions
    if user.type_utilisateur not in ['enseignant', 'coordination', 'admin']:
        messages.error(request, "Vous n'avez pas la permission de valider des paiements.")
        return redirect('index')
    
    paiement = get_object_or_404(PaiementCours, id=paiement_id)
    
    if request.method == 'POST':
        paiement.statut = 'valide'
        paiement.valideur = user
        paiement.date_validation = timezone.now()
        paiement.save()
        messages.success(request, f"Le paiement pour '{paiement.cours.titre}' a été validé.")
        return redirect('detail_paiement', paiement_id=paiement.id)
    
    context = {
        'paiement': paiement,
    }
    
    return render(request, 'etudiant/paiements/valider_paiement.html', context)


@login_required(login_url='login')
def refuser_paiement(request, paiement_id):
    """Vue pour refuser un paiement (admin/enseignant/coordination uniquement)"""
    user = request.user
    
    # Vérifier les permissions
    if user.type_utilisateur not in ['enseignant', 'coordination', 'admin']:
        messages.error(request, "Vous n'avez pas la permission de refuser des paiements.")
        return redirect('index')
    
    paiement = get_object_or_404(PaiementCours, id=paiement_id)
    
    if request.method == 'POST':
        paiement.statut = 'refuse'
        paiement.valideur = user
        paiement.date_validation = timezone.now()
        if 'commentaires' in request.POST:
            commentaires = request.POST.get('commentaires', '')
            if paiement.commentaires:
                paiement.commentaires += f"\n\n[Refusé le {timezone.now().strftime('%d/%m/%Y %H:%M')}]: {commentaires}"
            else:
                paiement.commentaires = f"[Refusé le {timezone.now().strftime('%d/%m/%Y %H:%M')}]: {commentaires}"
        paiement.save()
        messages.warning(request, f"Le paiement pour '{paiement.cours.titre}' a été refusé.")
        return redirect('detail_paiement', paiement_id=paiement.id)
    
    context = {
        'paiement': paiement,
    }
    
    return render(request, 'etudiant/paiements/refuser_paiement.html', context)

