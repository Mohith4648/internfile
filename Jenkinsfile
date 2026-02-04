pipeline {
    agent any

    environment {
        // --- SONARQUBE CONFIGURATION ---
        // 1. PROJECT KEY: Found on your project home page (e.g., Mohith4648_internfile)
        SONAR_PROJECT_KEY = "mohith468"
        // 2. ORGANIZATION KEY: Found in My Organizations (e.g., mohith4648)
        SONAR_ORG_KEY     = "mohith4648"
        
        // --- DOCKER CONFIGURATION ---
        IMAGE_NAME = "intern-project"
        TAG = "v1"
        CRED_ID = "dockerentry" // This matches your Jenkins Credential ID
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                cleanWs()
                git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
            }
        }

        stage('2. SonarQube Analysis') {
            steps {
                // This 'sonar-token' must be a "Secret Text" in Jenkins
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                    script {
                        echo "Running SonarQube Analysis..."
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
                        sh "docker build -t ${DOCKER_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                        sh "echo '${DOCKER_PASS}' | docker login -u '${DOCKER_USER}' --password-stdin"
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
                    sh "docker rm -f prod-site || true"
                    sh "docker run -d --name prod-site -p 8081:80 ${DOCKER_USER}/${env.IMAGE_NAME}:${env.TAG}"
                }
            }
        }
    }
}
