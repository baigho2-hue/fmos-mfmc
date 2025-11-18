#!/bin/bash
# Script d'initialisation du site sur Render
# À exécuter dans le Shell Render

echo "=========================================="
echo "🚀 Initialisation du Site FMOS-MFMC"
echo "=========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Étape 1 : Migrations
echo -e "${YELLOW}[1/4] Application des migrations...${NC}"
python manage.py migrate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'application des migrations${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Migrations appliquées${NC}"
echo ""

# Étape 2 : Vérifier l'état des migrations
echo -e "${YELLOW}[2/4] Vérification de l'état des migrations...${NC}"
python manage.py showmigrations | tail -5
echo ""

# Étape 3 : Créer un superutilisateur (si nécessaire)
echo -e "${YELLOW}[3/4] Création d'un superutilisateur...${NC}"
echo "Si un superutilisateur existe déjà, vous pouvez annuler (Ctrl+C) et passer à l'étape suivante"
python manage.py createsuperuser
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Superutilisateur non créé (peut-être déjà existant)${NC}"
fi
echo ""

# Étape 4 : Initialiser le programme DESMFMC
echo -e "${YELLOW}[4/4] Initialisation du programme DESMFMC...${NC}"
python manage.py init_programme_desmfmc_detaille
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'initialisation du programme${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Programme DESMFMC initialisé${NC}"
echo ""

# Étape 5 (Optionnelle) : Initialiser les coûts
echo -e "${YELLOW}[Optionnel] Initialisation des coûts de formations...${NC}"
read -p "Voulez-vous initialiser les coûts de formations ? (o/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    python manage.py init_couts_formations
    echo -e "${GREEN}✅ Coûts de formations initialisés${NC}"
fi
echo ""

# Résumé
echo "=========================================="
echo -e "${GREEN}✅ Initialisation terminée !${NC}"
echo "=========================================="
echo ""
echo "Prochaines étapes :"
echo "1. Accédez à l'admin : https://fmos-mfmc.onrender.com/admin/"
echo "2. Connectez-vous avec votre superutilisateur"
echo "3. Vérifiez que tout fonctionne correctement"
echo ""

