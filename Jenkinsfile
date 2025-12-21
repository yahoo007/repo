pipeline {
    agent any

    environment {
        // Définition du nom de l'image avec l'ID du build pour éviter les conflits
        REGISTRY_USER = "votre-username" // Optionnel : pour un futur push
        IMAGE_NAME    = "test-docker-web-app"
        IMAGE_TAG     = "${env.BUILD_ID}"
        FULL_IMAGE    = "${IMAGE_NAME}:${IMAGE_TAG}"
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
                    // Construction de l'image
                    sh "docker build -t ${FULL_IMAGE} ."
                    // On tag aussi en 'latest' pour faciliter les tests locaux
                    sh "docker tag ${FULL_IMAGE} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('3. Scan de Sécurité (Trivy)') {
            steps {
                script {
                    echo "Lancement du scan Trivy sur ${FULL_IMAGE}..."
                    // On monte le socket docker pour que Trivy puisse analyser l'image locale
                    // --exit-code 1 : fait échouer le pipeline si des vulnérabilités CRITICAL sont trouvées
                    sh """
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            -v \$HOME/.cache:/root/.cache \
                            aquasec/trivy:latest image \
                            --severity CRITICAL \
                            --exit-code 1 \
                            ${FULL_IMAGE}
                    """
                }
            }
        }

        stage('4. Déploiement (Simulation)') {
            // Cette étape ne s'exécutera que si le scan Trivy est réussi (exit code 0)
            steps {
                echo "Déploiement de l'image sécurisée : ${FULL_IMAGE}"
                // Exemple : sh "docker-compose up -d" ou un push vers un registre
            }
        }
    }

    post {
        always {
            echo "Nettoyage final..."
            // Supprime le binaire temporaire mentionné dans vos logs
            sh "rm -f ./docker-compose-temp"
        }
        success {
            echo "Pipeline terminé avec succès !"
        }
        failure {
            echo "Le pipeline a échoué. Vérifiez les vulnérabilités Trivy ou les logs Docker."
        }
        cleanup {
            // Optionnel : Supprime l'image construite pour ne pas saturer le disque du serveur
            sh "docker rmi ${FULL_IMAGE} ${IMAGE_NAME}:latest || true"
        }
    }
}