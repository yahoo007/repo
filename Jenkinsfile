pipeline {
    agent any

    environment {
        // Définition des variables pour l'image
        IMAGE_NAME = "test-docker-web-app"
        IMAGE_TAG  = "${env.BUILD_ID}"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('1. Préparation') {
            steps {
                echo "Nettoyage et récupération du code..."
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
                    echo "Nettoyage du cache Trivy et scan..."
                    // Nettoyage du cache (nouvelle syntaxe)
                    sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest clean --all"
                    
                    // Scan de l'image (échoue si faille CRITICAL)
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

        stage('4. Déploiement avec .env') {
            steps {
                script {
                    echo "Nettoyage des anciens conteneurs..."
                    // Arrête et supprime l'application si elle existe déjà
                    sh "docker stop mon-app-container || true"
                    sh "docker rm mon-app-container || true"
                    
                    echo "Lancement de l'application..."
                    // Utilisation du fichier .env pour injecter les mots de passe
                    // --network devsecops-net : pour communiquer avec le conteneur 'db'
                    // --env-file .env : pour lire les variables de configuration
                    sh """
                        docker run -d \
                            -p 8081:5000 \
                            --name mon-app-container \
                            --network devsecops-net \
                            --env-file .env \
                            -e DB_HOST=db \
                            ${FULL_IMAGE}
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Nettoyage final..."
            sh "rm -f ./docker-compose-temp"
            // On ne supprime pas l'image immédiatement ici pour que le conteneur puisse tourner
        }
        success {
            echo "Déploiement réussi ! Disponible sur http://localhost:8081"
        }
        failure {
            echo "Le pipeline a échoué. Vérifiez l'espace disque ou les logs Trivy."
        }
        cleanup {
            // Supprime les images inutilisées pour libérer de l'espace sur le serveur
            sh "docker image prune -f"
        }
    }
}