pipeline {
    agent any

    environment {
        // ID du secret que vous avez créé dans Jenkins
        DB_PASS_SECRET = credentials('DB_PASSWORD')
    }

    stages {
        stage('1. Nettoyage') {
            steps {
                echo 'Nettoyage des anciens conteneurs...'
                // Utilisation de "docker compose" (avec espace)
                sh 'docker compose down --remove-orphans || true'
            }
        }

        stage('2. Build & Security Scan') {
            steps {
                echo 'Construction de l\'image...'
                sh 'docker compose build'
                
                echo 'Scan de sécurité avec Trivy...'
                sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity CRITICAL mon-app-v2:latest"
            }
        }

        stage('3. Déploiement Sécurisé') {
            steps {
                echo 'Lancement des services...'
                // On utilise la variable d'environnement définie plus haut
                sh "DB_PASSWORD=${DB_PASS_SECRET} docker compose up -d --force-recreate"
            }
        }
    }

    post {
        success {
            echo 'Déploiement réussi sur http://localhost:8081'
        }
        failure {
            echo 'Le pipeline a échoué. Vérifiez les erreurs ci-dessus.'
        }
    }
}