pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = "mohith4648"
        IMAGE_NAME = "intern-project"
        TAG = "v1"
        CRED_ID = "mohith4648" 
    }

    stages {
        stage('1. Force Cache Clear & Pull') {
            steps {
                script {
                    // This is the "Magic Line" that deletes the @script and @tmp folders
                    // It clears the hidden cache that keeps the Selenium error alive
                    sh "rm -rf ${WORKSPACE}@* || true"
                    
                    // Clean the main workspace
                    cleanWs()
                    
                    // Pull the fresh code
                    git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
                }
            }
        }

        stage('2. Build Application') {
            steps {
                // Since your files are in the root, we don't need dir('UI')
                sh "docker build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG} ."
            }
        }

        stage('3. Push to Hub') {
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

        stage('4. Deploy') {
            steps {
                sh "docker rm -f prod-site || true"
                sh "docker run -d --name prod-site -p 8081:80 ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                echo "SUCCESS: intern-project is live on port 8081"
            }
        }
    }
}
