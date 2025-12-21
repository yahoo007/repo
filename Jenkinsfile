pipeline {
    agent any

    environment {
        IMAGE_NAME = "test-docker-web-app"
        IMAGE_TAG  = "${env.BUILD_ID}"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('1. Préparation') {
            steps {
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

        stage('3. Scan de Sécurité (Trivy)') {
            steps {
                script {
                    echo "Nettoyage du cache Trivy et lancement du scan..."
                    // Nouvelle syntaxe Trivy pour vider le cache et libérer de la place
                    sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest clean --all"

                    // Lancement du scan
                    sh """
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

        stage('4. Déploiement') {
            steps {
                echo "Déploiement réussi !"
            }
        }
    }

    post {
        always {
            sh "rm -f ./docker-compose-temp"
            // On nettoie l'image tout de suite pour ne pas saturer le disque
            sh "docker rmi ${FULL_IMAGE} ${IMAGE_NAME}:latest || true"
        }
        cleanup {
            // Nettoyage agressif des résidus Docker
            sh "docker image prune -f"
        }
    }
}