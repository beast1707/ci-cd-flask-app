pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/beast1707/ci-cd-flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ayushd1707/guestbook:latest .'
            }
        }

        stage('Push Image') {
            steps {
                sh 'docker login -u ayushd1707 -p Beast@1707'
                sh 'docker push ayushd1707/guestbook:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                expression { false }   // ✅ DISABLE THIS STAGE COMPLETELY
            }
            steps {
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl apply -f service.yaml'
            }
        }
    }
}
