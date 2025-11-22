# core/views_paiements.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from apps.utilisateurs.models_formation import PaiementFormation, Formation
from apps.utilisateurs.forms import PaiementFormationForm


@login_required(login_url='login')
def mes_paiements(request):
    """Vue pour afficher la liste des paiements de l'étudiant"""
    user = request.user
    
    # Vérifier que l'utilisateur est un étudiant
    if user.type_utilisateur != 'etudiant':
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard_etudiant')
    
    # Récupérer tous les paiements de l'étudiant
    paiements = PaiementFormation.objects.filter(etudiant=user).order_by('-date_paiement')
    
    # Statistiques
    total_paiements = paiements.count()
    paiements_valides = paiements.filter(statut='valide').count()
    paiements_en_attente = paiements.filter(statut='en_attente').count()
    montant_total = sum(p.montant for p in paiements.filter(statut='valide'))
    
    context = {
        'paiements': paiements,
        'total_paiements': total_paiements,
        'paiements_valides': paiements_valides,
        'paiements_en_attente': paiements_en_attente,
        'montant_total': montant_total,
    }
    
    return render(request, 'etudiant/paiements/mes_paiements.html', context)


@login_required(login_url='login')
def creer_paiement(request):
    """Vue pour créer un nouveau paiement"""
    user = request.user
    
    # Vérifier que l'utilisateur est un étudiant
    if user.type_utilisateur != 'etudiant':
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard_etudiant')
    
    if request.method == 'POST':
        form = PaiementFormationForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.etudiant = user
            paiement.statut = 'en_attente'
            paiement.save()
            messages.success(
                request,
                f"Votre paiement de {paiement.montant} FCFA pour la formation '{paiement.formation.nom}' a été enregistré. "
                "Il sera validé par l'administration sous peu."
            )
            return redirect('mes_paiements')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = PaiementFormationForm(user=user)
    
    # Récupérer les formations disponibles
    formations_disponibles = Formation.objects.filter(actif=True).order_by('nom')
    
    context = {
        'form': form,
        'formations_disponibles': formations_disponibles,
    }
    
    return render(request, 'etudiant/paiements/creer_paiement.html', context)


@login_required(login_url='login')
def detail_paiement(request, paiement_id):
    """Vue pour afficher les détails d'un paiement"""
    user = request.user
    
    paiement = get_object_or_404(PaiementFormation, id=paiement_id)
    
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
    
    paiement = get_object_or_404(PaiementFormation, id=paiement_id)
    
    if request.method == 'POST':
        paiement.statut = 'valide'
        paiement.valideur = user
        paiement.date_validation = timezone.now()
        paiement.save()
        messages.success(request, f"Le paiement pour '{paiement.formation.nom}' a été validé.")
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
    
    paiement = get_object_or_404(PaiementFormation, id=paiement_id)
    
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
        messages.warning(request, f"Le paiement pour '{paiement.formation.nom}' a été refusé.")
        return redirect('detail_paiement', paiement_id=paiement.id)
    
    context = {
        'paiement': paiement,
    }
    
    return render(request, 'etudiant/paiements/refuser_paiement.html', context)

