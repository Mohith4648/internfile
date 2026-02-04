pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = "mohith4648"
        IMAGE_NAME = "intern-project"
        TAG = "v1"
        CRED_ID = "mohith4648" 
    }

    stages {
        stage('1. Environment Reset & Pull') {
            steps {
                script {
                    // Force delete the hidden cache folders
                    sh "rm -rf ${WORKSPACE}@* || true"
                    cleanWs()
                    git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
                }
            }
        }

        stage('2. Build Application Image') {
            steps {
                // Building from the root where your Dockerfile now lives
                sh "docker build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG} ."
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
                sh "docker rm -f prod-site || true"
                sh "docker run -d --name prod-site -p 8081:80 ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                
                echo "------------------------------------------------------------"
                echo "SUCCESS: intern-project is live at http://localhost:8081"
                echo "------------------------------------------------------------"
            }
        }
    }

    post {
        always {
            // Keep the server clean
            sh "rm -rf ${WORKSPACE}@*"
        }
    }
}
