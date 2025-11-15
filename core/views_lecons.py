"""
Vues pour gérer les leçons, quiz, commentaires et progression
"""
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db import transaction
from decimal import Decimal

from apps.utilisateurs.models_formation import (
    Lecon, ProgressionLecon, CommentaireLecon, QuizLecon,
    QuestionQuiz, ReponseQuestion, ReponseEtudiantQuiz, ResultatQuiz
)


@login_required
@require_POST
def marquer_lecon_vue(request, lecon_id):
    """Marque une leçon comme vue et met à jour la progression"""
    lecon = get_object_or_404(Lecon, pk=lecon_id, actif=True)
    
    # Vérifier l'accès
    if not request.user.est_etudiant() and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Accès refusé'}, status=403)
    
    # Vérifier que l'étudiant a accès à cette leçon
    classe_obj = request.user.get_classe_obj()
    if not request.user.is_superuser and (not classe_obj or lecon.cours.classe != classe_obj):
        return JsonResponse({'success': False, 'error': 'Accès refusé'}, status=403)
    
    # Récupérer ou créer la progression
    progression, created = ProgressionLecon.objects.get_or_create(
        etudiant=request.user,
        lecon=lecon,
        defaults={
            'statut': 'en_cours',
            'date_debut': timezone.now(),
        }
    )
    
    # Mettre à jour la progression
    pourcentage = int(request.POST.get('pourcentage', progression.pourcentage_completion))
    temps_passe = int(request.POST.get('temps_passe', progression.temps_passe_minutes))
    
    progression.pourcentage_completion = min(100, max(0, pourcentage))
    progression.temps_passe_minutes = max(0, temps_passe)
    
    if pourcentage >= 100:
        progression.statut = 'termine'
        if not progression.date_fin:
            progression.date_fin = timezone.now()
    elif progression.statut == 'non_commence':
        progression.statut = 'en_cours'
        if not progression.date_debut:
            progression.date_debut = timezone.now()
    
    progression.save()
    
    return JsonResponse({
        'success': True,
        'statut': progression.get_statut_display(),
        'pourcentage': progression.pourcentage_completion,
        'temps_passe': progression.temps_passe_minutes,
    })


@login_required
@require_POST
def ajouter_commentaire_lecon(request, lecon_id):
    """Ajoute un commentaire sur une leçon"""
    lecon = get_object_or_404(Lecon, pk=lecon_id, actif=True)
    
    # Vérifier l'accès
    classe_obj = request.user.get_classe_obj()
    if not request.user.is_superuser and (not classe_obj or lecon.cours.classe != classe_obj):
        messages.error(request, "Vous n'avez pas accès à cette leçon.")
        return redirect('detail_cours', cours_id=lecon.cours.id)
    
    contenu = request.POST.get('contenu', '').strip()
    parent_id = request.POST.get('parent_id')
    
    if not contenu:
        messages.error(request, "Le commentaire ne peut pas être vide.")
        return redirect('detail_cours', cours_id=lecon.cours.id)
    
    parent = None
    if parent_id:
        try:
            parent = CommentaireLecon.objects.get(pk=parent_id, lecon=lecon)
        except CommentaireLecon.DoesNotExist:
            pass
    
    CommentaireLecon.objects.create(
        lecon=lecon,
        auteur=request.user,
        contenu=contenu,
        parent=parent
    )
    
    messages.success(request, "Commentaire ajouté avec succès.")
    return redirect('detail_cours', cours_id=lecon.cours.id)


@login_required
def passer_quiz(request, quiz_id):
    """Affiche et permet de passer un quiz"""
    quiz = get_object_or_404(QuizLecon, pk=quiz_id, actif=True)
    
    # Vérifier l'accès
    classe_obj = request.user.get_classe_obj()
    if not request.user.est_etudiant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('mes_cours')
    
    if not request.user.is_superuser and (not classe_obj or quiz.lecon.cours.classe != classe_obj):
        messages.error(request, "Vous n'avez pas accès à ce quiz.")
        return redirect('mes_cours')
    
    # Récupérer ou créer le résultat
    resultat, created = ResultatQuiz.objects.get_or_create(
        etudiant=request.user,
        quiz=quiz,
        defaults={
            'date_debut': timezone.now(),
        }
    )
    
    # Récupérer les questions avec leurs réponses possibles
    questions = QuestionQuiz.objects.filter(quiz=quiz).order_by('ordre').prefetch_related('reponses_possibles')
    
    # Récupérer les réponses existantes de l'étudiant
    reponses_existantes = ReponseEtudiantQuiz.objects.filter(
        etudiant=request.user,
        quiz=quiz
    ).prefetch_related('reponses_choisies')
    reponses_dict = {r.question_id: r for r in reponses_existantes}
    
    if request.method == 'POST' and not resultat.termine:
        # Traiter les réponses
        with transaction.atomic():
            total_points = Decimal('0.00')
            
            for question in questions:
                if question.type_reponse == 'texte_libre':
                    reponse_texte = request.POST.get(f'question_{question.id}', '').strip()
                    if reponse_texte:
                        reponse_etudiant, _ = ReponseEtudiantQuiz.objects.get_or_create(
                            etudiant=request.user,
                            quiz=quiz,
                            question=question,
                            defaults={'reponse_texte': reponse_texte}
                        )
                        if not _:
                            reponse_etudiant.reponse_texte = reponse_texte
                            reponse_etudiant.save()
                        # Pour les questions texte libre, on ne peut pas corriger automatiquement
                        # L'enseignant devra le faire manuellement
                        total_points += question.points
                        reponse_etudiant.points_obtenus = question.points
                        reponse_etudiant.save()
                
                elif question.type_reponse == 'choix_unique':
                    reponse_id = request.POST.get(f'question_{question.id}')
                    if reponse_id:
                        try:
                            reponse_choisie = ReponseQuestion.objects.get(pk=reponse_id, question=question)
                            reponse_etudiant, _ = ReponseEtudiantQuiz.objects.get_or_create(
                                etudiant=request.user,
                                quiz=quiz,
                                question=question
                            )
                            reponse_etudiant.reponses_choisies.clear()
                            reponse_etudiant.reponses_choisies.add(reponse_choisie)
                            
                            # Calculer les points
                            if reponse_choisie.est_correcte:
                                points = question.points
                            else:
                                points = Decimal('0.00')
                            
                            reponse_etudiant.points_obtenus = points
                            reponse_etudiant.save()
                            total_points += points
                        except (ReponseQuestion.DoesNotExist, ValueError):
                            pass
                
                elif question.type_reponse == 'vrai_faux':
                    reponse_valeur = request.POST.get(f'question_{question.id}')
                    if reponse_valeur in ['vrai', 'faux']:
                        # Trouver la réponse correspondante
                        reponses_possibles = question.reponses_possibles.all()
                        reponse_correcte = None
                        for rep in reponses_possibles:
                            if (reponse_valeur == 'vrai' and rep.texte.lower() in ['vrai', 'true', 'oui', 'yes']) or \
                               (reponse_valeur == 'faux' and rep.texte.lower() in ['faux', 'false', 'non', 'no']):
                                if rep.est_correcte:
                                    reponse_correcte = rep
                                break
                        
                        # Si pas trouvé, chercher la réponse correcte
                        if not reponse_correcte:
                            reponse_correcte = reponses_possibles.filter(est_correcte=True).first()
                        
                        reponse_etudiant, _ = ReponseEtudiantQuiz.objects.get_or_create(
                            etudiant=request.user,
                            quiz=quiz,
                            question=question,
                            defaults={'reponse_texte': reponse_valeur}
                        )
                        if not _:
                            reponse_etudiant.reponse_texte = reponse_valeur
                            reponse_etudiant.save()
                        
                        # Calculer les points
                        if reponse_correcte:
                            # Vérifier si la réponse de l'étudiant correspond à la bonne réponse
                            bonne_reponse_texte = reponse_correcte.texte.lower()
                            if (reponse_valeur == 'vrai' and bonne_reponse_texte in ['vrai', 'true', 'oui', 'yes']) or \
                               (reponse_valeur == 'faux' and bonne_reponse_texte in ['faux', 'false', 'non', 'no']):
                                points = question.points
                            else:
                                points = Decimal('0.00')
                        else:
                            # Par défaut, donner les points si on ne peut pas vérifier
                            points = Decimal('0.00')
                        
                        reponse_etudiant.points_obtenus = points
                        reponse_etudiant.save()
                        total_points += points
                
                elif question.type_reponse == 'choix_multiple':
                    reponse_ids = request.POST.getlist(f'question_{question.id}')
                    if reponse_ids:
                        reponses_choisies = ReponseQuestion.objects.filter(
                            pk__in=reponse_ids,
                            question=question
                        )
                        reponse_etudiant, _ = ReponseEtudiantQuiz.objects.get_or_create(
                            etudiant=request.user,
                            quiz=quiz,
                            question=question
                        )
                        reponse_etudiant.reponses_choisies.set(reponses_choisies)
                        
                        # Calculer les points (toutes les bonnes réponses doivent être choisies)
                        reponses_correctes = question.reponses_possibles.filter(est_correcte=True)
                        reponses_choisies_correctes = reponses_choisies.filter(est_correcte=True)
                        
                        if reponses_correctes.count() == reponses_choisies_correctes.count() and \
                           reponses_choisies.count() == reponses_correctes.count():
                            points = question.points
                        else:
                            points = Decimal('0.00')
                        
                        reponse_etudiant.points_obtenus = points
                        reponse_etudiant.save()
                        total_points += points
            
            # Mettre à jour le résultat
            resultat.note_finale = total_points
            resultat.pourcentage = (total_points / quiz.note_maximale * 100).quantize(Decimal('0.01'))
            resultat.termine = True
            resultat.date_fin = timezone.now()
            resultat.save()
            
            messages.success(request, f"Quiz terminé ! Votre note : {total_points}/{quiz.note_maximale}")
            return redirect('resultat_quiz', quiz_id=quiz.id)
    
    return render(request, 'etudiant/passer_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'reponses_dict': reponses_dict,
        'resultat': resultat,
    })


@login_required
def resultat_quiz(request, quiz_id):
    """Affiche le résultat d'un quiz"""
    quiz = get_object_or_404(QuizLecon, pk=quiz_id, actif=True)
    
    # Vérifier l'accès
    classe_obj = request.user.get_classe_obj()
    if not request.user.est_etudiant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('mes_cours')
    
    if not request.user.is_superuser and (not classe_obj or quiz.lecon.cours.classe != classe_obj):
        messages.error(request, "Vous n'avez pas accès à ce quiz.")
        return redirect('mes_cours')
    
    resultat = get_object_or_404(ResultatQuiz, quiz=quiz, etudiant=request.user)
    questions = QuestionQuiz.objects.filter(quiz=quiz).order_by('ordre').prefetch_related('reponses_possibles')
    reponses_etudiant = ReponseEtudiantQuiz.objects.filter(
        etudiant=request.user,
        quiz=quiz
    ).prefetch_related('reponses_choisies')
    reponses_dict = {r.question_id: r for r in reponses_etudiant}
    
    return render(request, 'etudiant/resultat_quiz.html', {
        'quiz': quiz,
        'resultat': resultat,
        'questions': questions,
        'reponses_dict': reponses_dict,
    })

