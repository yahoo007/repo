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
                    sh "docker build -t ${FULL_IMAGE} ."
                    sh "docker tag ${FULL_IMAGE} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('3. Scan de Sécurité (Trivy)') {
            steps {
                script {
                    // Nettoyage recommandé avant le scan
                    sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest clean --all"
                    
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

        stage('4. Déploiement Sécurisé') {
            steps {
                // Utilisation du secret Jenkins pour pallier l'absence du fichier .env
                withCredentials([file(credentialsId: 'DOTENV_FILE', variable: 'ENV_FILE')]) {
                    script {
                        echo "Nettoyage des anciens conteneurs..."
                        sh "docker stop mon-app-container || true"
                        sh "docker rm mon-app-container || true"
                        
                        echo "Lancement avec injection des secrets..."
                        // On utilise la variable ENV_FILE qui pointe vers le fichier stocké par Jenkins
                        sh """
                            docker run -d \
                                -p 8081:5000 \
                                --name mon-app-container \
                                --network devsecops-net \
                                --env-file ${ENV_FILE} \
                                -e DB_HOST=db \
                                ${FULL_IMAGE}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            sh "rm -f ./docker-compose-temp"
        }
        cleanup {
            sh "docker image prune -f"
        }
    }
}