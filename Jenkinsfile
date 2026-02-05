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
        
        // --- KUBERNETES CONFIGURATION ---
        K8S_DEPLOYMENT_NAME = "intern-proj-deployment"
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                cleanWs()
                git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
            }
        }

        stage('2. SonarQube Static Analysis') {
            steps {
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
                        echo "Building and Pushing Image to Docker Hub..."
                        sh "docker build -t ${DOCKER_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                        sh "echo '${DOCKER_PASS}' | docker login -u '${DOCKER_USER}' --password-stdin"
                        sh "docker push ${DOCKER_USER}/${env.IMAGE_NAME}:${env.TAG}"
                        sh "docker logout"
                    }
                }
            }
        }

        stage('4. Kubernetes Production Deployment') {
            steps {
                script {
                    echo "Deploying to Kubernetes Cluster..."
                    
                    // 1. Apply the Deployment and Service configuration
                    sh "kubectl apply -f deployment.yaml"
                    
                    // 2. Force a Rolling Update to use the latest image pushed
                    sh "kubectl rollout restart deployment/${env.K8S_DEPLOYMENT_NAME}"
                    
                    // 3. Wait for the rollout to complete to ensure zero-downtime
                    sh "kubectl rollout status deployment/${env.K8S_DEPLOYMENT_NAME}"
                    
                    echo "------------------------------------------------------------"
                    echo "SUCCESS: Kubernetes Deployment Complete with 3 Replicas!"
                    echo "Verify pods: kubectl get pods"
                    echo "------------------------------------------------------------"
                }
            }
        }
    }
    
    post {
        failure {
            echo "Pipeline failed. Check SonarQube or Docker logs."
        }
    }
}
