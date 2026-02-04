pipeline {
    agent any

    environment {
        // We define the Image name, but leave the username to be pulled from credentials
        IMAGE_NAME = "intern-project"
        TAG = "v1"
        CRED_ID = "dockerentry" 
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                cleanWs()
                git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
            }
        }

        stage('2. Build Application Image') {
            steps {
                // Here we use the credentials to get the username for the tag
                withCredentials([usernamePassword(credentialsId: "${env.CRED_ID}", 
                                 passwordVariable: 'DOCKER_PASS', 
                                 usernameVariable: 'DOCKER_USER')]) {
                    script {
                        echo "Building Docker Image for user: ${DOCKER_USER}"
                        // Tagging the image using the variable from Jenkins credentials
                        sh "docker build -t ${DOCKER_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                    }
                }
            }
        }

        stage('3. Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${env.CRED_ID}", 
                                 passwordVariable: 'DOCKER_PASS', 
                                 usernameVariable: 'DOCKER_USER')]) {
                    sh """
                        echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                        docker push ${DOCKER_USER}/${env.IMAGE_NAME}:${env.TAG}
                        docker logout
                    """
                }
            }
        }

        stage('4. Production Deployment') {
            steps {
                // Again, using the credential variable for the deployment
                withCredentials([usernamePassword(credentialsId: "${env.CRED_ID}", 
                                 passwordVariable: 'DOCKER_PASS', 
                                 usernameVariable: 'DOCKER_USER')]) {
                    script {
                        sh "docker rm -f prod-site || true"
                        sh "docker run -d --name prod-site -p 8081:80 ${DOCKER_USER}/${env.IMAGE_NAME}:${env.TAG}"
                        
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
}
