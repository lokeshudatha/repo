pipeline {
    agent any

    environment {
        APP_NAME = "python-app"
        IMAGE = "yourdockerhubusername/python-app:${env.BUILD_NUMBER}"
        VM_IP = "GCP_PYTHON_VM_IP"  // Replace with terraform output
        SSH_USER = "debian"         // Default for Debian image
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'python', url: 'https://github.com/lokeshudatha/repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dir('python-app') {
                        sh "docker build -t ${IMAGE} ."
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh """
                        echo "$PASS" | docker login -u "$USER" --password-stdin
                        docker push ${IMAGE}
                    """
                }
            }
        }

        stage('Deploy to GCP Python VM') {
            steps {
                sshagent(['gcp-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${SSH_USER}@${VM_IP} "
                            sudo docker pull ${IMAGE} &&
                            sudo docker rm -f python-app || true &&
                            sudo docker run -d -p 80:5000 --name python-app ${IMAGE}
                        "
                    """
                }
            }
        }
    }

    post {
        success { echo 'Python App Deployed Successfully on GCP VM' }
        failure { echo 'Deployment Failed' }
    }
}
