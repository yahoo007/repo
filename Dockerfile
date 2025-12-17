pipeline {
    agent any
    tools { dockerTool 'docker' } // Utilise l'outil Docker qu'on a configuré ensemble

    stages {
        stage('Build Image') {
            steps {
                // On build l'image Docker
                sh 'docker build -t mon-app-image:latest .'
            }
        }
        stage('Deploy') {
            steps {
                // On nettoie l'ancien conteneur et on lance le nouveau
                sh 'docker stop mon-app-container || true'
                sh 'docker rm mon-app-container || true'
                sh 'docker run -d --name mon-app-container -p 8081:80 mon-app-image:latest'
            }
        }
    }
}