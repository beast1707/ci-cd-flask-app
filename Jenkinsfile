pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/your-username/ci-cd-flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t your-dockerhub-username/guestbook:latest .'
            }
        }

        stage('Push Image') {
            steps {
                sh 'docker login -u your-dockerhub-username -p your-dockerhub-password'
                sh 'docker push your-dockerhub-username/guestbook:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl apply -f service.yaml'
            }
        }
    }
}
