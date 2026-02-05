pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = "Mohith4648_internfile"
        SONAR_ORG_KEY     = "mohith4648"
        IMAGE_NAME = "intern-project"
        TAG = "v1"
        CRED_ID = "dockerentry"
        K8S_DEPLOYMENT_NAME = "intern-proj-deployment"
        
        // --- NEW: Kubernetes Credential ID ---
        // You will create this 'secret file' in the Jenkins UI
        K8S_CRED_ID = "k8s-kubeconfig" 
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                cleanWs()
                git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
            }
        }

        // ... Stages 2 & 3 (SonarQube & Docker) stay exactly the same ...

        stage('4. Kubernetes Production Deployment') {
            steps {
                // This binds your uploaded kubeconfig file to a temporary path variable
                withCredentials([file(credentialsId: "${env.K8S_CRED_ID}", variable: 'KUBECONFIG')]) {
                    script {
                        echo "Deploying to Kubernetes via Remote Jenkins..."
                        
                        // Check if kubectl exists; if not, you may need to ask your 'Sir' to install it
                        sh "kubectl version --client"
                        
                        // Use the injected KUBECONFIG to authenticate
                        sh "kubectl --kubeconfig=${KUBECONFIG} apply -f deployment.yaml"
                        sh "kubectl --kubeconfig=${KUBECONFIG} rollout restart deployment/${env.K8S_DEPLOYMENT_NAME}"
                        sh "kubectl --kubeconfig=${KUBECONFIG} rollout status deployment/${env.K8S_DEPLOYMENT_NAME}"
                        
                        echo "------------------------------------------------------------"
                        echo "SUCCESS: Highly Available Deployment Complete!"
                        echo "------------------------------------------------------------"
                    }
                }
            }
        }
    }
}
