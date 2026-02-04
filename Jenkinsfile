
pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = "mohith4648"
        IMAGE_NAME = "intern-project"
        TAG = "v1"
        // Ensure this ID matches the name you gave your credential in Jenkins
        CRED_ID = "mohith4648" 
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                // Safely cleans the workspace
                cleanWs()
                git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
            }
        }

        stage('2. Build Application Image') {
            steps {
                script {
                    // Builds from the root since you moved your files out of the UI folder
                    echo "Building Docker Image: ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                    sh "docker build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                }
            }
        }

        stage('3. Push to Docker Hub') {
            steps {
                // Securely pulls your password from Jenkins settings instead of hardcoding it
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
                    sh "docker rm -f prod-site || true"
                    sh "docker run -d --name prod-site -p 8081:80 ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                    
                    echo """
                    ------------------------------------------------------------
                    PROJECT STATUS: DEPLOYED SUCCESSFULLY
                    URL: http://localhost:8081
                    ------------------------------------------------------------
                    """
                }
            }
        }
    }
}
