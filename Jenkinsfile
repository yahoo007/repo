pipeline {
    agent any

    tools {
        // On utilise l'outil Docker qu'on a configuré dans Jenkins
        dockerTool 'docker'
    }

    stages {
        stage('Nettoyage') {
            steps {
                // On arrête l'ancien conteneur s'il tourne déjà
                sh 'docker stop mon-app-web || true'
                sh 'docker rm mon-app-web || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                // On construit l'image à partir du Dockerfile présent dans le dossier
                sh 'docker build --no-cache -t mon-app-image:latest .'
                sh 'docker build -t mon-image-web:latest .'
            }
        }

        stage('Deploy Conteneur') {
            steps {
                // On lance le nouveau conteneur sur le port 8081
                sh 'docker run -d --name mon-app-web -p 8081:80 mon-image-web:latest'
                echo "Succès ! Application disponible sur http://localhost:8081"
            }
        }
    }
}