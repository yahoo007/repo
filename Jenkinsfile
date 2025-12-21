pipeline {
    agent any

    environment {
        // Définition dynamique du nom de l'image
        IMAGE_NAME = "test-docker-web-app"
        IMAGE_TAG  = "${env.BUILD_ID}"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('1. Préparation') {
            steps {
                echo "Nettoyage de l'espace de travail..."
                deleteDir()
                checkout scm
            }
        }

        stage('2. Build Docker') {
            steps {
                script {
                    echo "Construction de l'image : ${FULL_IMAGE}"
                    sh "docker build -t ${FULL_IMAGE} ."
                    sh "docker tag ${FULL_IMAGE} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('3. Scan de Sécurité (Trivy) - Mode Survie') {
            steps {
                script {
                    echo "Réinitialisation du cache Trivy et lancement du scan..."
                    // On exécute deux commandes : 
                    // 1. --reset pour vider le cache qui sature le disque
                    // 2. Le scan sans montage de cache externe pour minimiser l'écriture disque
                    sh """
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image --reset

                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image \
                            --severity CRITICAL \
                            --exit-code 1 \
                            ${FULL_IMAGE}
                    """
                }
            }
        }

        stage('4. Déploiement (Simulation)') {
            steps {
                echo "Déploiement réussi de l'image sécurisée : ${FULL_IMAGE}"
            }
        }
    }

    post {
        always {
            echo "Nettoyage des fichiers et des images temporaires..."
            sh "rm -f ./docker-compose-temp"
            // Suppression de l'image locale pour libérer immédiatement l'espace
            sh "docker rmi ${FULL_IMAGE} ${IMAGE_NAME}:latest || true"
        }
        failure {
            echo "Le pipeline a échoué. Vérifiez l'espace disque (df -h) ou les failles CRITICAL."
        }
        cleanup {
            // Nettoyage des images Docker 'dangling' (orphelines) pour regagner de la place
            sh "docker image prune -f"
        }
    }
}