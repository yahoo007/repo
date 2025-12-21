pipeline {
    agent any

    environment {
        // Nom de l'image définit dans le docker-compose.yml
        IMAGE_NAME = "mon-app-v2:latest"
    }

    stages {
        stage('1. Nettoyage') {
            steps {
                echo 'Arrêt des anciens conteneurs pour éviter les conflits...'
                // Le "|| true" évite que le build échoue si aucun conteneur n'existe encore
                sh 'docker-compose down --remove-orphans || true'
            }
        }

        stage('2. Build & Security Scan') {
            steps {
                echo 'Construction de l\'image et analyse des vulnérabilités...'
                sh 'docker-compose build'
                
                // Scan Trivy : cherche uniquement les failles CRITIQUES
                // On utilise l'image de Trivy pour scanner l'image qu'on vient de builder
                sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity CRITICAL ${IMAGE_NAME}"
            }
        }

        stage('3. Déploiement Sécurisé') {
            steps {
                echo 'Déploiement avec injection des secrets Jenkins...'
                
                // Récupère le secret "DB_PASSWORD" depuis Jenkins et le met dans DB_PASS_JENKINS
                withCredentials([string(credentialsId: 'DB_PASSWORD', variable: 'DB_PASS_JENKINS')]) {
                    
                    // On passe le secret au docker-compose au moment du lancement
                    // On force la recréation pour être sûr que le secret est pris en compte
                    sh "DB_PASSWORD=${DB_PASS_JENKINS} docker-compose up -d --force-recreate"
                }
            }
        }
    }

    post {
        success {
            echo 'Félicitations ! Le déploiement V2 est opérationnel.'
        }
        failure {
            echo 'Le build ou le scan de sécurité a échoué. Vérifiez les logs.'
        }
    }
}