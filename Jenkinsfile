stage('1. Nettoyage') {
    steps {
        echo 'Arrêt des anciens conteneurs...'
        // On remplace le tiret par un espace
        sh 'docker compose down --remove-orphans || true'
    }
}

stage('2. Build & Security Scan') {
    steps {
        echo 'Construction...'
        sh 'docker compose build'
        sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity CRITICAL mon-app-v2:latest"
    }
}

stage('3. Déploiement Sécurisé') {
    steps {
        withCredentials([string(credentialsId: 'DB_PASSWORD', variable: 'DB_PASS_JENKINS')]) {
            // On remplace le tiret par un espace ici aussi
            sh "DB_PASSWORD=${DB_PASS_JENKINS} docker compose up -d --force-recreate"
        }
    }
}