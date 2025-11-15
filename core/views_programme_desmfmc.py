# core/views_programme_desmfmc.py
"""
Vues pour le programme DESMFMC structuré sur 4 ans
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.utilisateurs.models_formation import Formation
from apps.utilisateurs.models_programme_desmfmc import (
    JalonProgramme, ModuleProgramme, SuiviProgressionProgramme
)


@login_required(login_url='login')
def programme_desmfmc_complet(request):
    """Vue pour afficher le programme complet DESMFMC sur 4 ans"""
    # Récupérer la formation DESMFMC
    try:
        formation_desmfmc = Formation.objects.get(code='DESMFMC', actif=True)
    except Formation.DoesNotExist:
        messages.error(request, "Le programme DESMFMC n'est pas encore configuré.")
        return redirect('formations')
    
    # Récupérer tous les jalons du programme
    jalons = JalonProgramme.objects.filter(
        formation=formation_desmfmc
    ).order_by('annee', 'ordre').prefetch_related('modules__cours_programme__cours')
    
    # Organiser les jalons par année
    programme_par_annee = {}
    for jalon in jalons:
        if jalon.annee not in programme_par_annee:
            programme_par_annee[jalon.annee] = []
        programme_par_annee[jalon.annee].append(jalon)
    
    # Si l'utilisateur est un étudiant, récupérer sa progression
    progression_etudiant = None
    progression_dict = {}
    progression_par_annee = {}
    
    if request.user.est_etudiant():
        progression_etudiant = SuiviProgressionProgramme.objects.filter(
            etudiant=request.user
        ).select_related('jalon')
        
        # Créer un dictionnaire pour accès rapide par jalon
        progression_dict = {p.jalon.id: p for p in progression_etudiant}
        
        # Calculer la progression par année
        for annee in range(1, 5):
            jalons_annee = [j for j in jalons if j.annee == annee]
            progressions_annee = [p for p in progression_etudiant if p.jalon.annee == annee]
            jalons_termines = sum(1 for p in progressions_annee if p.statut in ['termine', 'valide'])
            progression_pct = (jalons_termines / len(jalons_annee) * 100) if jalons_annee else 0
            progression_par_annee[annee] = {'pourcentage': round(progression_pct, 1)}

    # Statistiques globales du programme
    stats_programme = {
        'total_jalons': jalons.count(),
        'total_modules': ModuleProgramme.objects.filter(jalon__formation=formation_desmfmc).count(),
        'total_heures': sum(j.volume_horaire_total for j in jalons),
    }
    
    context = {
        'formation': formation_desmfmc,
        'programme_par_annee': programme_par_annee,
        'progression_dict': progression_dict,
        'progression_par_annee': progression_par_annee,
        'stats_programme': stats_programme,
        'user': request.user,
    }
    
    return render(request, 'programme/programme_desmfmc_complet.html', context)


@login_required(login_url='login')
def detail_jalon(request, jalon_id):
    """Détail d'un jalon avec modules et cours"""
    jalon = get_object_or_404(JalonProgramme, pk=jalon_id)
    
    # Récupérer les modules du jalon
    modules = ModuleProgramme.objects.filter(
        jalon=jalon,
        actif=True
    ).order_by('ordre').prefetch_related(
        'cours_programme__cours',
        'objectifs_module',
        'competences_module'
    )
    
    # Si étudiant, récupérer la progression
    progression = None
    if request.user.est_etudiant():
        progression, created = SuiviProgressionProgramme.objects.get_or_create(
            etudiant=request.user,
            jalon=jalon
        )
    
    context = {
        'jalon': jalon,
        'modules': modules,
        'progression': progression,
        'user': request.user,
    }
    
    return render(request, 'programme/detail_jalon.html', context)


@login_required(login_url='login')
def ma_progression_programme(request):
    """Vue pour l'étudiant : sa progression dans le programme complet"""
    if not request.user.est_etudiant():
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    # Récupérer la formation DESMFMC
    try:
        formation_desmfmc = Formation.objects.get(code='DESMFMC', actif=True)
    except Formation.DoesNotExist:
        messages.error(request, "Le programme DESMFMC n'est pas encore configuré.")
        return redirect('dashboard_etudiant')
    
    # Récupérer tous les jalons
    jalons = JalonProgramme.objects.filter(
        formation=formation_desmfmc
    ).order_by('annee', 'ordre')
    
    # Récupérer la progression de l'étudiant
    progressions = SuiviProgressionProgramme.objects.filter(
        etudiant=request.user,
        jalon__formation=formation_desmfmc
    ).select_related('jalon')
    
    progression_dict = {p.jalon.id: p for p in progressions}
    
    # Organiser par année avec progression
    progression_par_annee = {}
    for jalon in jalons:
        if jalon.annee not in progression_par_annee:
            progression_par_annee[jalon.annee] = []
        progression_par_annee[jalon.annee].append({
            'jalon': jalon,
            'progression': progression_dict.get(jalon.id)
        })
    
    # Calculer la progression globale
    total_jalons = jalons.count()
    jalons_termines = sum(1 for p in progressions if p.statut in ['termine', 'valide'])
    progression_globale = (jalons_termines / total_jalons * 100) if total_jalons > 0 else 0
    
    # Statistiques par année
    stats_par_annee = {}
    for annee in range(1, 5):
        jalons_annee = [j for j in jalons if j.annee == annee]
        progressions_annee = [p for p in progressions if p.jalon.annee == annee]
        jalons_termines_annee = sum(1 for p in progressions_annee if p.statut in ['termine', 'valide'])
        progression_annee = (jalons_termines_annee / len(jalons_annee) * 100) if jalons_annee else 0
        
        stats_par_annee[annee] = {
            'total': len(jalons_annee),
            'termines': jalons_termines_annee,
            'progression': round(progression_annee, 1)
        }
    
    context = {
        'formation': formation_desmfmc,
        'progression_par_annee': progression_par_annee,
        'progression_globale': round(progression_globale, 1),
        'stats_par_annee': stats_par_annee,
        'total_jalons': total_jalons,
        'jalons_termines': jalons_termines,
    }
    
    return render(request, 'programme/ma_progression_programme.html', context)

