pipeline {
    agent any

    environment {
        // --- SONARQUBE CONFIGURATION ---
        SONAR_PROJECT_KEY = "Mohith4648_internfile"
        SONAR_ORG_KEY     = "mohith4648"
        
        // --- DOCKER CONFIGURATION ---
        IMAGE_NAME = "intern-project"
        TAG = "v1"
        CRED_ID = "dockerentry" // For your Docker Hub login
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                cleanWs()
                // Pulls your tourism portal code
                git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
            }
        }

        stage('2. SonarQube Static Analysis') {
            steps {
                // This 'sonar-token' must match the ID you just created in Jenkins Credentials
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                    script {
                        echo "Starting Code Analysis on SonarCloud..."
                        sh """
                            docker run --rm \
                            -v ${WORKSPACE}:/usr/src \
                            -e SONAR_TOKEN=${SONAR_TOKEN} \
                            -e SONAR_HOST_URL="https://sonarcloud.io" \
                            sonarsource/sonar-scanner-cli \
                            -Dsonar.projectKey=${env.SONAR_PROJECT_KEY} \
                            -Dsonar.organization=${env.SONAR_ORG_KEY} \
                            -Dsonar.sources=.
                        """
                    }
                }
            }
        }

        stage('3. Build & Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${env.CRED_ID}", 
                                 passwordVariable: 'DOCKER_PASS', 
                                 usernameVariable: 'DOCKER_USER')]) {
                    script {
                        echo "Building Docker Image for ${DOCKER_USER}..."
                        sh "docker build -t ${DOCKER_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                        
                        echo "Logging into Docker Hub..."
                        sh "echo '${DOCKER_PASS}' | docker login -u '${DOCKER_USER}' --password-stdin"
                        
                        echo "Pushing Image..."
                        sh "docker push ${DOCKER_USER}/${env.IMAGE_NAME}:${env.TAG}"
                        sh "docker logout"
                    }
                }
            }
        }

        stage('4. Production Deployment') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${env.CRED_ID}", 
                                 passwordVariable: 'DOCKER_PASS', 
                                 usernameVariable: 'DOCKER_USER')]) {
                    script {
                        echo "Deploying to Port 8081..."
                        // Remove old container if it exists
                        sh "docker rm -f prod-site || true"
                        
                        // Run the updated container
                        sh "docker run -d --name prod-site -p 8081:80 ${DOCKER_USER}/${env.IMAGE_NAME}:${env.TAG}"
                        
                        echo "------------------------------------------------------------"
                        echo "SUCCESS: Build and Deployment Complete!"
                        echo "Check SonarCloud for results: https://sonarcloud.io/project/overview?id=${env.SONAR_PROJECT_KEY}"
                        echo "------------------------------------------------------------"
                    }
                }
            }
        }
    }
} 
