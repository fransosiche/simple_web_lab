#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

error_exit() {
    echo -e "${RED}❌  $1${NC}"
    exit 1
}

success_msg() {
    echo -e "${GREEN}✅ $1${NC}"
}

info_msg() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Vérifier les prérequis
check_prerequisites() {
    # Vérifier si Docker est installé
    if ! command -v docker &> /dev/null; then
        info_msg "Docker n'est pas installé"
        echo "Installation :"
        echo "  sudo apt-get update && sudo apt-get install docker.io"
        error_exit "Veuillez installer Docker et réessayer"
    fi

    # Vérifier si Docker Compose est installé
    if ! command -v docker-compose &> /dev/null; then
        info_msg "Docker Compose n'est pas installé"
        echo "Installation :"
        echo "  sudo apt-get install docker-compose"
        error_exit "Veuillez installer Docker Compose et réessayer"
    fi

    # Vérifier si Docker daemon est en cours d'exécution
    if ! docker info &> /dev/null; then
        info_msg "Le daemon Docker n'est pas en cours d'exécution"
        echo "Démarrage :"
        echo "  sudo systemctl start docker"
        error_exit "Veuillez démarrer Docker et réessayer"
    fi

    success_msg "Vérification des prérequis terminée"
}

# Nettoyer l'environnement
cleanup() {
    info_msg "Nettoyage de l'environnement..."
    docker-compose down &> /dev/null
}

# Démarrer le lab
start_lab() {
    info_msg "Démarrage du lab..."
    docker-compose up -d --build
    
    # Attendre que le conteneur soit prêt
    sleep 3
    
    # Vérifier si le conteneur est en cours d'exécution
    if ! docker ps | grep -q vulnerable-lab_web_1; then
        error_exit "Le conteneur n'a pas démarré correctement"
    fi
}

# Afficher les informations du lab
show_lab_info() {
    CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' vulnerable-lab_web_1)
    
    echo -e "\n${GREEN}🚀 Lab prêt !${NC}"
    echo "================================================"
    echo -e "${YELLOW}📡 IP du conteneur:${NC} $CONTAINER_IP"
    echo "================================================"
    echo -e "${YELLOW}💡 Pour arrêter:${NC}"
    echo -e "${RED} docker-compose down ${NC}"
    echo -e "================================================"
}

# Fonction principale
main()  {
    check_prerequisites
    cleanup
    start_lab
    show_lab_info
}

# Exécuter le script
main
