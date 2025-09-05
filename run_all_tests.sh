#!/usr/bin/env bash
# Script pour compiler les programmes COBOL et exécuter tous les tests

set -e  # Arrêter en cas d'erreur

# Définition des couleurs pour la sortie
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Automatisation des Tests pour la Migration COBOL vers Python ===${NC}"

# 1. Vérifier la présence de GnuCOBOL
echo -e "\n${YELLOW}1. Vérification de GnuCOBOL...${NC}"
if command -v cobc >/dev/null 2>&1; then
    echo -e "${GREEN}✓ GnuCOBOL est installé${NC}"
    cobc --version | head -n 1
else
    echo -e "${RED}✗ GnuCOBOL n'est pas installé${NC}"
    echo "Pour installer GnuCOBOL:"
    echo "  - macOS: brew install gnu-cobol"
    echo "  - Ubuntu/Debian: apt-get install gnucobol"
    echo "  - Fedora/RHEL: dnf install gnucobol"
    exit 1
fi

# 2. Compiler les programmes COBOL
echo -e "\n${YELLOW}2. Compilation des programmes COBOL...${NC}"
if [ -f cobol/accountsystem ]; then
    echo "Suppression de l'ancien exécutable..."
    rm cobol/accountsystem
fi

echo "Compilation en cours..."
cobc -x -o cobol/accountsystem cobol/main.cob cobol/operations.cob cobol/data.cob
echo -e "${GREEN}✓ Compilation COBOL réussie${NC}"

# 3. Exécuter les tests unitaires Python
echo -e "\n${YELLOW}3. Exécution des tests unitaires Python...${NC}"
python3 run_tests.py --unit-only
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Tests unitaires Python réussis${NC}"
else
    echo -e "${RED}✗ Échec des tests unitaires Python${NC}"
    exit 1
fi

# 4. Exécuter les tests E2E
echo -e "\n${YELLOW}4. Exécution des tests End-to-End...${NC}"
python3 run_tests.py --e2e-only
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Tests End-to-End réussis${NC}"
else
    echo -e "${RED}✗ Échec des tests End-to-End${NC}"
    echo "Vérifiez que les comportements COBOL et Python sont identiques"
    exit 1
fi

# 5. Résumé
echo -e "\n${YELLOW}=== Résumé des Tests ===${NC}"
echo -e "${GREEN}✓ Tous les tests ont réussi${NC}"
echo "La migration de COBOL vers Python maintient la parité fonctionnelle"
echo -e "${YELLOW}Consultez les rapports détaillés pour plus d'informations${NC}"
