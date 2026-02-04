pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = "mohith4648"
        // Replace this with your actual Docker Hub Token/Password
        DOCKER_HUB_PASS = "dckr_pat__8huaWVfjTtjjc4g622LRU0Nvp0" 
        
        IMAGE_NAME = "intern-project"
        TAG = "v1"
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                cleanWs()
                // Pulling your clean code from the internfile repo
                git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
            }
        }

        stage('2. Build Application Image') {
            steps {
                script {
                    echo "Building Docker Image..."
                    // Building from the root where your Dockerfile is
                    sh "docker build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                }
            }
        }

        stage('3. Push to Docker Hub') {
            steps {
                script {
                    echo "Logging into Docker Hub and Pushing..."
                    sh """
                        echo "${env.DOCKER_HUB_PASS}" | docker login -u "${env.DOCKER_HUB_USER}" --password-stdin
                        docker push ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}
                        docker logout
                    """
                }
            }
        }

        stage('4. Production Deployment') {
            steps {
                script {
                    // Remove old container to avoid port 8081 conflicts
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

    post {
        always {
            // Clean up temporary Jenkins folders
            sh "rm -rf ${WORKSPACE}@*"
        }
    }
}
