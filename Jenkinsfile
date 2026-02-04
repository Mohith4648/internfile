pipeline {
    agent any

    environment {
        // Professional Metadata
        DOCKER_HUB_USER = "mohith4648"
        IMAGE_NAME = "intern-project"
        TAG = "v1"
        // Ensure this ID matches your Jenkins Credentials ID
        CRED_ID = "mohith4648" 
    }

    stages {
        stage('1. Environment Cleanup & Pull') {
            steps {
                // Cleans the workspace to prevent old file "ghosts"
                cleanWs()
                // Directly pulls your code from the internfile repo
                git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
            }
        }

        stage('2. Build & Remove Unused Artifacts') {
            steps {
                script {
                    // Logic to delete unused files before building the image
                    sh """
                        rm -f pom.xml || true
                        rm -rf archive_automation || true
                        echo "Workspace cleaned of unused artifacts."
                    """
                    
                    // Build the Docker image using your Nginx Dockerfile
                    // Note: If Dockerfile is in the root, we don't need dir('UI')
                    sh "docker build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                }
            }
        }

        stage('3. Secure Registry Push') {
            steps {
                // Using Jenkins Credentials Store for security
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
                    // Stop existing container to avoid port conflicts
                    sh "docker rm -f prod-site || true"
                    
                    // Run the new container on port 8081
                    sh "docker run -d --name prod-site -p 8081:80 ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                    
                    echo """
                    ------------------------------------------------------------
                    DEPLOID SUCCESSFULLY: intern-project
                    ACCESS URL: http://localhost:8081
                    DOCKER IMAGE: ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}
                    ------------------------------------------------------------
                    """
                }
            }
        }
    }

    post {
        always {
            // Final cleanup of the @script and @tmp folders to keep the server clean
            sh "rm -rf ${WORKSPACE}@*"
        }
    }
}
