pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('lokesh/python-app', '.')
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_TOKEN')]) {
                    sh '''
                    echo $DOCKER_TOKEN | docker login -u lokeshudatha --password-stdin
                    docker tag lokesh/python-app lokeshudatha/python-app:latest
                    docker push lokeshudatha/python-app:latest
                    '''
                }
            }
        }
        stage('Deploy with Terraform') {
            steps {
                dir('terraform/python') {
                    sh '''
                    terraform init
                    terraform apply -auto-approve
                    '''
                }
            }
        }
    }
}
