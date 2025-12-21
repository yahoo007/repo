pipeline {
    agent any

    environment {
        DB_PASS_SECRET = credentials('DB_PASSWORD')
        // On définit un chemin local pour le binaire compose
        DOCKER_COMPOSE_BIN = "./docker-compose-temp"
    }

    stages {
        stage('0. Préparation Docker Compose') {
            steps {
                echo 'Téléchargement de Docker Compose...'
                // Télécharge le binaire directement dans le dossier de travail
                sh 'curl -SL https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-linux-x86_64 -o ${DOCKER_COMPOSE_BIN}'
                sh 'chmod +x ${DOCKER_COMPOSE_BIN}'
                sh "${DOCKER_COMPOSE_BIN} version"
            }
        }

        stage('1. Nettoyage') {
            steps {
                echo 'Nettoyage des anciens conteneurs...'
                sh "${DOCKER_COMPOSE_BIN} down || true"
            }
        }

        stage('2. Build & Scan') {
            steps {
                echo 'Construction de l\'image...'
                sh "${DOCKER_COMPOSE_BIN} build"
                
                echo 'Scan de sécurité avec Trivy...'
                sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity CRITICAL mon-app-v2:latest"
            }
        }

        stage('3. Déploiement Sécurisé') {
            steps {
                echo 'Lancement des services...'
                sh "DB_PASSWORD=${DB_PASS_SECRET} ${DOCKER_COMPOSE_BIN} up -d"
            }
        }
    }

    post {
        always {
            echo 'Nettoyage du binaire temporaire...'
            sh "rm -f ${DOCKER_COMPOSE_BIN}"
        }
    }
}