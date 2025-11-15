# apps/utilisateurs/utils.py
import random
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import CodeVerification, Utilisateur
from .models_programme_desmfmc import CSComUCentre, StageRotationDES


def generer_code_verification(user):
    """
    Génère un code de vérification à 6 chiffres et l'envoie par email
    """
    # Générer un code à 6 chiffres
    code = str(random.randint(100000, 999999))
    
    # Créer le code de vérification (expire dans 10 minutes)
    code_verif = CodeVerification.objects.create(
        user=user,
        code=code,
        expire_le=timezone.now() + timedelta(minutes=10)
    )
    
    # Envoyer l'email
    sujet = "Code de vérification - FMOS MFMC"
    message = f"""
Bonjour {user.get_full_name() or user.username},

Votre code de vérification pour vous connecter à la plateforme FMOS MFMC est :

{code}

Ce code est valide pendant 10 minutes.

Si vous n'avez pas demandé ce code, veuillez ignorer cet email.

Cordialement,
L'équipe FMOS MFMC
"""
    
    try:
        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@fmos-mfmc.ml',
            [user.email],
            fail_silently=False,
        )
        
        # En mode développement, afficher aussi le code dans la console pour faciliter les tests
        if settings.DEBUG:
            print(f"\n{'='*60}")
            print(f"CODE DE VERIFICATION (MODE DEVELOPPEMENT)")
            print(f"{'='*60}")
            print(f"Utilisateur: {user.username} ({user.email})")
            print(f"Code: {code}")
            print(f"Valide jusqu'à: {code_verif.expire_le}")
            print(f"{'='*60}\n")
        
        return code_verif
    except Exception as e:
        # En cas d'erreur d'envoi, ne pas supprimer le code en mode développement
        # pour permettre de le récupérer manuellement
        if settings.DEBUG:
            print(f"\n{'='*60}")
            print(f"ERREUR ENVOI EMAIL - CODE DISPONIBLE (MODE DEVELOPPEMENT)")
            print(f"{'='*60}")
            print(f"Utilisateur: {user.username} ({user.email})")
            print(f"Code: {code}")
            print(f"Valide jusqu'à: {code_verif.expire_le}")
            print(f"Erreur: {e}")
            print(f"{'='*60}\n")
            # Ne pas supprimer le code en mode développement
            return code_verif
        else:
            # En production, supprimer le code en cas d'erreur
            code_verif.delete()
            raise e


def verifier_code(user, code_saisi):
    """
    Vérifie si le code saisi est valide pour l'utilisateur
    """
    try:
        code_verif = CodeVerification.objects.filter(
            user=user,
            code=code_saisi,
            utilise=False
        ).order_by('-cree_le').first()
        
        if code_verif and code_verif.est_valide():
            # Marquer le code comme utilisé
            code_verif.utilise = True
            code_verif.save()
            return True
        return False
    except Exception:
        return False


def attribuer_stages_cscom_aleatoire(etudiants, annee, periode, date_debut=None, date_fin=None):
    """
    Attribue aléatoirement des stages CSCom-U aux étudiants pour une année et période données.
    Respecte les contraintes :
    - Un étudiant ne peut pas faire deux fois le même CSCom-U
    - Un étudiant ne peut pas faire deux stages urbains la même année
    
    Args:
        etudiants: QuerySet d'étudiants
        annee: Année du DES (2 ou 3)
        periode: Période (1 ou 2)
        date_debut: Date de début du stage (optionnel)
        date_fin: Date de fin du stage (optionnel)
    
    Returns:
        dict: {
            'reussite': bool,
            'attributions': list de StageRotationDES créés,
            'erreurs': list de messages d'erreur
        }
    """
    from django.db import transaction
    
    erreurs = []
    attributions = []
    
    # Récupérer les CSCom-U actifs par type
    cscom_urbains = list(CSComUCentre.objects.filter(type_centre='urbain', actif=True))
    cscom_ruraux = list(CSComUCentre.objects.filter(type_centre='rural', actif=True))
    
    if not cscom_urbains:
        erreurs.append("Aucun CSCom-U urbain disponible")
    if not cscom_ruraux:
        erreurs.append("Aucun CSCom-U rural disponible")
    
    if erreurs:
        return {'reussite': False, 'attributions': [], 'erreurs': erreurs}
    
    # Pour chaque étudiant, déterminer le type de stage nécessaire
    # En année 2 et 3, chaque étudiant doit avoir 1 stage urbain et 1 stage rural par an
    type_necessaire = 'urbain' if periode == 1 else 'rural'
    
    try:
        with transaction.atomic():
            for etudiant in etudiants:
                # Récupérer les stages existants de cet étudiant pour cette année
                stages_annee = StageRotationDES.objects.filter(etudiant=etudiant, annee=annee)
                
                # Vérifier si l'étudiant a déjà un stage urbain pour cette année
                if type_necessaire == 'urbain':
                    stage_urbain_existant = stages_annee.filter(centre__type_centre='urbain').exclude(periode=periode).first()
                    if stage_urbain_existant:
                        erreurs.append(
                            f"{etudiant.username}: A déjà un stage urbain pour l'année {annee} "
                            f"(période {stage_urbain_existant.periode})"
                        )
                        continue
                
                # Récupérer les CSCom-U déjà utilisés par cet étudiant (toutes années confondues)
                # pour éviter qu'il fasse deux fois le même CSCom-U
                stages_tous = StageRotationDES.objects.filter(etudiant=etudiant)
                cscom_deja_utilises = set(stages_tous.values_list('centre_id', flat=True))
                
                # Filtrer les CSCom-U disponibles selon le type nécessaire
                if type_necessaire == 'urbain':
                    cscom_disponibles = [c for c in cscom_urbains if c.id not in cscom_deja_utilises]
                else:
                    cscom_disponibles = [c for c in cscom_ruraux if c.id not in cscom_deja_utilises]
                
                if not cscom_disponibles:
                    erreurs.append(
                        f"{etudiant.username}: Aucun CSCom-U {type_necessaire} disponible "
                        f"(tous déjà utilisés ou épuisés)"
                    )
                    continue
                
                # Tirage au sort
                centre_attribue = random.choice(cscom_disponibles)
                
                # Vérifier qu'il n'existe pas déjà un stage pour cette année/période
                stage_existant = stages_annee.filter(periode=periode).first()
                
                if stage_existant:
                    # Mettre à jour le stage existant
                    stage_existant.centre = centre_attribue
                    stage_existant.attribue_automatiquement = True
                    if date_debut:
                        stage_existant.date_debut = date_debut
                    if date_fin:
                        stage_existant.date_fin = date_fin
                    stage_existant.save()
                    attributions.append(stage_existant)
                else:
                    # Créer un nouveau stage
                    stage = StageRotationDES.objects.create(
                        etudiant=etudiant,
                        annee=annee,
                        periode=periode,
                        centre=centre_attribue,
                        date_debut=date_debut,
                        date_fin=date_fin,
                        attribue_automatiquement=True
                    )
                    attributions.append(stage)
            
            return {
                'reussite': len(erreurs) == 0,
                'attributions': attributions,
                'erreurs': erreurs
            }
    
    except Exception as e:
        erreurs.append(f"Erreur lors de l'attribution : {str(e)}")
        return {'reussite': False, 'attributions': [], 'erreurs': erreurs}

