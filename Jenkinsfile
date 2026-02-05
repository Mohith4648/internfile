pipeline {
    agent any

    environment {
        // --- SONARQUBE CONFIGURATION ---
        SONAR_PROJECT_KEY = "Mohith4648_internfile"
        SONAR_ORG_KEY     = "mohith4648"
        
        // --- DOCKER CONFIGURATION ---
        IMAGE_NAME = "intern-project"
        TAG = "v1"
        CRED_ID = "dockerentry" // Docker Hub credentials ID in Jenkins
        
        // --- KUBERNETES CONFIGURATION ---
        K8S_DEPLOYMENT_NAME = "intern-proj-deployment"
        // Path to your config file inside your GitHub repo
        KUBECONFIG_PATH = "scripts/myconfig.yaml" 
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                cleanWs()
                // Pulls your code from GitHub
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
                    echo "Deploying to Kubernetes using Config from GitHub..."
                    
                    // Check if the config file actually exists in your repo
                    if (fileExists(env.KUBECONFIG_PATH)) {
                        // 1. Apply the Deployment and Service
                        sh "kubectl --kubeconfig=${env.KUBECONFIG_PATH} apply -f deployment.yaml"
                        
                        // 2. Restart Pods to pull the fresh v1 image
                        sh "kubectl --kubeconfig=${env.KUBECONFIG_PATH} rollout restart deployment/${env.K8S_DEPLOYMENT_NAME}"
                        
                        // 3. Status check
                        sh "kubectl --kubeconfig=${env.KUBECONFIG_PATH} rollout status deployment/${env.K8S_DEPLOYMENT_NAME}"
                        
                        echo "------------------------------------------------------------"
                        echo "SUCCESS: Self-Healing Kubernetes Deployment Complete!"
                        echo "------------------------------------------------------------"
                    } else {
                        error "ERROR: ${env.KUBECONFIG_PATH} not found in repository! Please upload it to the scripts/ folder."
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline execution finished."
        }
        success {
            echo "Project is live on Kubernetes!"
        }
        failure {
            echo "Pipeline failed. Check Jenkins logs for details."
        }
    }
}
