pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = "mohith4648"
        IMAGE_NAME = "intern-project"
        TAG = "v1"
        // Using the ID you created in Manage Jenkins
        CRED_ID = "dockerentry" 
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                // Built-in clean is much faster and won't hang
                cleanWs()
                git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
            }
        }

        stage('2. Build Application Image') {
            steps {
                script {
                    echo "Building Docker Image: ${env.IMAGE_NAME}"
                    // Building from the root directory (.)
                    sh "docker build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                }
            }
        }

        stage('3. Push to Docker Hub') {
            steps {
                // Securely using your 'dockerentry' credentials
                withCredentials([string(credentialsId: "${env.CRED_ID}", variable: 'DOCKER_HUB_PASS')]) {
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
                script {
                    // Remove old container to avoid port conflicts
                    sh "docker rm -f prod-site || true"
                    
                    // Deploy to port 8081
                    sh "docker run -d --name prod-site -p 8081:80 ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                    
                    echo """
                    ------------------------------------------------------------
                    PROJECT STATUS: DEPLOYED SUCCESSFULLY
                    ACCESS URL: http://localhost:8081
                    ------------------------------------------------------------
                    """
                }
            }
        }
    }
}
