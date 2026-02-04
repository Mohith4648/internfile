pipeline {
    agent any

    environment {
        // We reference the ID you created in Jenkins Credentials (e.g., 'docker-hub-creds')
        DOCKER_HUB_USER = "mohith4648"
        IMAGE_NAME = "intern-file"
        TAG = "1.0.0"
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                cleanWs()
                // Ensure the URL matches your current Tourism repository
                git branch: 'main', url: 'https://github.com/Mohith4648/tourisum-project.git'
            }
        }

        stage('2. Docker Image Build') {
            steps {
                dir('UI') {
                    echo "Building Image: ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                    sh "docker build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                }
            }
        }

        stage('3. Push to Docker Hub') {
            steps {
                // 'docker-hub-creds' is the ID you gave your credentials in Jenkins
                withCredentials([string(credentialsId: 'docker-hub-creds', variable: 'DOCKER_HUB_PASS')]) {
                    sh """
                        echo "${DOCKER_HUB_PASS}" | docker login -u "${env.DOCKER_HUB_USER}" --password-stdin
                        docker push ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}
                        docker logout
                    """
                }
            }
        }

        stage('4. Production Deployment') {
            steps {
                sh "docker rm -f prod-site || true"
                sh "docker run -d --name prod-site -p 8081:80 ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                
                echo "------------------------------------------------------------"
                echo " TOURISM PROJECT DEPLOYED SUCCESSFULLY"
                echo " Access URL: http://localhost:8081"
                echo " Build Status: SUCCESS"
                echo "------------------------------------------------------------"
            }
        }
    }
}
