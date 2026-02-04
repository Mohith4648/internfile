pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = "mohith4648"
        IMAGE_NAME = "intern-project"
        TAG = "v1"
        // Double check: This must match the ID in your Jenkins Credentials list
        CRED_ID = "mohith4648" 
    }

    stages {
        stage('1. Force Reset & Pull') {
            steps {
                script {
                    // KILL THE CACHE: This removes the hidden @script folders holding old Selenium code
                    sh "rm -rf ${WORKSPACE}@* || true"
                    
                    // Clean the main workspace
                    cleanWs()
                    
                    // Pull fresh code from GitHub
                    git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
                }
            }
        }

        stage('2. Build Application Image') {
            steps {
                script {
                    // Clean up any stray files before building
                    sh "rm -f pom.xml || true"
                    
                    // Build the Docker image from the ROOT directory
                    echo "Starting Docker build for intern-project..."
                    sh "docker build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                }
            }
        }

        stage('3. Secure Registry Push') {
            steps {
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
                    // Remove old container if it exists
                    sh "docker rm -f prod-site || true"
                    
                    // Deploy the new container
                    sh "docker run -d --name prod-site -p 8081:80 ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                    
                    echo """
                    ------------------------------------------------------------
                    DEPLOYED SUCCESSFULLY: intern-project
                    ACCESS URL: http://localhost:8081
                    STATUS: PRODUCTION IS LIVE
                    ------------------------------------------------------------
                    """
                }
            }
        }
    }

    post {
        always {
            // Final housekeeping to keep the Jenkins server healthy
            sh "rm -rf ${WORKSPACE}@*"
        }
    }
}
