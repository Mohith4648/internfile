pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = "mohith4648"
        IMAGE_NAME = "tourism-travel-portal"
        TAG = "v1"
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                cleanWs()
                // Replace with your Tourism repo URL
                git branch: 'main', url: 'https://github.com/Mohith4648/tourisum-project.git'
            }
        }

        stage('2. Build Application Image') {
            steps {
                dir('UI') {
                    // This builds using the standard 'Dockerfile' in your UI folder
                    sh "docker build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                }
            }
        }

        stage('3. Push to Docker Hub') {
            steps {
                // Using the Credential ID you created in Jenkins
                withCredentials([string(credentialsId: 'docker-hub-creds', variable: 'DOCKER_HUB_PASS')]) {
                    sh """
                        echo "${DOCKER_HUB_PASS}" | docker login -u "${env.DOCKER_HUB_USER}" --password-stdin
                        docker push ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}
                        docker logout
                    """
                }
            }
        }

        stage('4. Deploy to Production') {
            steps {
                sh "docker rm -f prod-site || true"
                sh "docker run -d --name prod-site -p 8081:80 ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                
                echo "SUCCESS: Tourism Project is live at Port 8081"
            }
        }
    }
}
