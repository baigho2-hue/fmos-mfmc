# apps/utilisateurs/utils_devise.py
"""
Utilitaires pour la conversion de devises et la détection de localisation
"""
import json
import urllib.request
import urllib.error
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

# Mapping des pays vers leurs devises principales
PAYS_DEVISE = {
    'ML': 'XOF',  # Mali - Franc CFA
    'SN': 'XOF',  # Sénégal - Franc CFA
    'CI': 'XOF',  # Côte d'Ivoire - Franc CFA
    'BF': 'XOF',  # Burkina Faso - Franc CFA
    'BJ': 'XOF',  # Bénin - Franc CFA
    'NE': 'XOF',  # Niger - Franc CFA
    'TG': 'XOF',  # Togo - Franc CFA
    'GN': 'GNF',  # Guinée - Franc guinéen
    'MR': 'MRU',  # Mauritanie - Ouguiya
    'CM': 'XAF',  # Cameroun - Franc CFA BEAC
    'TD': 'XAF',  # Tchad - Franc CFA BEAC
    'CF': 'XAF',  # Centrafrique - Franc CFA BEAC
    'CG': 'XAF',  # Congo - Franc CFA BEAC
    'GA': 'XAF',  # Gabon - Franc CFA BEAC
    'GQ': 'XAF',  # Guinée équatoriale - Franc CFA BEAC
    'CD': 'CDF',  # RDC - Franc congolais
    'FR': 'EUR',  # France - Euro
    'US': 'USD',  # États-Unis - Dollar
    'CA': 'CAD',  # Canada - Dollar canadien
    'GB': 'GBP',  # Royaume-Uni - Livre sterling
}

# Noms des devises
NOMS_DEVISES = {
    'XOF': 'Franc CFA (Ouest)',
    'XAF': 'Franc CFA (Centrale)',
    'FCFA': 'Franc CFA',
    'GNF': 'Franc guinéen',
    'MRU': 'Ouguiya',
    'CDF': 'Franc congolais',
    'EUR': 'Euro',
    'USD': 'Dollar américain',
    'CAD': 'Dollar canadien',
    'GBP': 'Livre sterling',
}

# Symboles des devises
SYMBOLES_DEVISES = {
    'XOF': 'FCFA',
    'XAF': 'FCFA',
    'FCFA': 'FCFA',
    'GNF': 'FG',
    'MRU': 'UM',
    'CDF': 'FC',
    'EUR': '€',
    'USD': '$',
    'CAD': 'C$',
    'GBP': '£',
}


def detecter_pays_par_ip(ip_address):
    """
    Détecte le pays à partir de l'adresse IP
    Utilise ip-api.com (gratuit, sans clé API)
    """
    if not ip_address or ip_address == '127.0.0.1':
        return 'ML'  # Par défaut, Mali
    
    cache_key = f'pays_ip_{ip_address}'
    pays = cache.get(cache_key)
    
    if pays:
        return pays
    
    try:
        # Utiliser ip-api.com (gratuit, 45 requêtes/minute)
        url = f'http://ip-api.com/json/{ip_address}?fields=countryCode'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            pays = data.get('countryCode', 'ML')
            cache.set(cache_key, pays, 3600 * 24)  # Cache pour 24h
            return pays
    except Exception as e:
        logger.warning(f"Erreur lors de la détection du pays pour IP {ip_address}: {e}")
    
    return 'ML'  # Par défaut, Mali


def obtenir_devise_par_pays(pays_code):
    """Obtient la devise d'un pays"""
    return PAYS_DEVISE.get(pays_code, 'XOF')  # Par défaut XOF


def obtenir_taux_change(devise_source='XOF', devise_cible='XOF'):
    """
    Obtient le taux de change entre deux devises
    Utilise exchangerate-api.com (gratuit, 1500 requêtes/mois)
    """
    if devise_source == devise_cible:
        return 1.0
    
    cache_key = f'taux_change_{devise_source}_{devise_cible}'
    taux = cache.get(cache_key)
    
    if taux:
        return taux
    
    try:
        # Utiliser exchangerate-api.com (gratuit)
        # Note: Pour XOF, on utilise EUR comme base car XOF est indexé sur EUR (1 EUR = 655.957 XOF)
        if devise_source == 'XOF':
            # Convertir XOF vers EUR puis vers la devise cible
            taux_xof_eur = 1 / 655.957  # 1 XOF = 1/655.957 EUR
            if devise_cible == 'EUR':
                taux = taux_xof_eur
            else:
                # Obtenir taux EUR vers devise cible
                try:
                    url = 'https://api.exchangerate-api.com/v4/latest/EUR'
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req, timeout=5) as response:
                        data = json.loads(response.read().decode())
                        taux_eur_cible = data.get('rates', {}).get(devise_cible, 1.0)
                        taux = taux_xof_eur * taux_eur_cible
                except:
                    taux = 1.0
        elif devise_cible == 'XOF':
            # Convertir devise source vers EUR puis vers XOF
            try:
                url = 'https://api.exchangerate-api.com/v4/latest/EUR'
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    taux_eur_source = 1 / data.get('rates', {}).get(devise_source, 1.0)
                    taux = taux_eur_source * 655.957  # 1 EUR = 655.957 XOF
            except:
                taux = 1.0
        else:
            # Conversion entre deux devises non XOF
            try:
                url = f'https://api.exchangerate-api.com/v4/latest/{devise_source}'
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    taux = data.get('rates', {}).get(devise_cible, 1.0)
            except:
                taux = 1.0
        
        # Cache pour 1 heure
        cache.set(cache_key, taux, 3600)
        return taux
        
    except Exception as e:
        logger.warning(f"Erreur lors de la récupération du taux de change: {e}")
        return 1.0


def convertir_montant(montant_fcfa, devise_cible='XOF', ip_address=None):
    """
    Convertit un montant en FCFA vers une devise cible
    Si ip_address est fourni, détecte automatiquement la devise
    """
    if ip_address:
        pays = detecter_pays_par_ip(ip_address)
        devise_cible = obtenir_devise_par_pays(pays)
    
    if devise_cible == 'XOF' or devise_cible == 'FCFA':
        return {
            'montant': montant_fcfa,
            'devise': 'FCFA',
            'symbole': 'FCFA',
            'nom_devise': 'Franc CFA',
            'taux': 1.0
        }
    
    taux = obtenir_taux_change('XOF', devise_cible)
    montant_converti = montant_fcfa * taux
    
    return {
        'montant': round(montant_converti, 2),
        'devise': devise_cible,
        'symbole': SYMBOLES_DEVISES.get(devise_cible, devise_cible),
        'nom_devise': NOMS_DEVISES.get(devise_cible, devise_cible),
        'taux': taux,
        'montant_original': montant_fcfa
    }


def formater_montant(montant, devise='FCFA', afficher_original=True):
    """
    Formate un montant avec sa devise
    """
    symbole = SYMBOLES_DEVISES.get(devise, devise)
    
    if isinstance(montant, dict):
        # Si c'est un résultat de conversion
        montant_aff = f"{montant['montant']:,.0f}".replace(',', ' ')
        resultat = f"{montant_aff} {montant['symbole']}"
        
        if afficher_original and 'montant_original' in montant and montant['devise'] != 'FCFA':
            resultat += f" (≈ {montant['montant_original']:,.0f} FCFA)"
        
        return resultat
    else:
        # Montant simple
        montant_aff = f"{montant:,.0f}".replace(',', ' ')
        return f"{montant_aff} {symbole}"

