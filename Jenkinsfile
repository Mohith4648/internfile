pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = "mohith4648"
        DOCKER_HUB_PASS = "dckr_pat__8huaWVfjTtjjc4g622LRU0Nvp0"   // Demo only
        IMAGE_NAME = "intern-project"
        TAG = "v1"
    }

    stages {

        // ============================
        // 1. CLEAN & CLONE
        // ============================
        stage('1. Setup & Checkout') {
            steps {
                cleanWs()
                git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
            }
        }

        // ============================
        // 2. BUILD APP IMAGE
        // ============================
        stage('2. Build App Image') {
            steps {
                dir('UI') {
                    sh """
                        docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG} .
                    """
                }
            }
        }

        // ============================
        // 3. BUILD SELENIUM IMAGE
        // ============================
        stage('3. Build Selenium Image') {
            steps {
                dir('UI') {
                    sh """
                        docker build -t my-selenium:latest \
                        -f tests/Dockerfile.selenium tests
                    """
                }
            }
        }

        // ============================
        // 4. RUN SELENIUM TEST
        // ============================
        stage('4. Selenium Quality Gate') {
            steps {
                script {

                    // Cleanup old containers
                    sh "docker rm -f test-con || true"

                    // Start App Container
                    sh """
                        docker run -d \
                        --name test-con \
                        -p 8085:80 \
                        ${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG}
                    """

                    try {

                        echo "Running Selenium Tests..."

                        // Run Selenium Container
                        sh """
                            docker run --rm \
                            --network host \
                            my-selenium:latest
                        """

                        echo "SELENIUM TEST PASSED ✅"

                    } catch (e) {

                        echo "SELENIUM TEST FAILED ❌"
                        error "Build Failed"

                    } finally {

                        // Cleanup
                        sh "docker rm -f test-con || true"
                    }
                }
            }
        }

        // ============================
        // 5. PUSH IMAGE
        // ============================
        stage('5. Push to DockerHub') {
            steps {
                sh """
                    echo "${DOCKER_HUB_PASS}" | docker login \
                    -u "${DOCKER_HUB_USER}" --password-stdin

                    docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG}

                    docker logout
                """
            }
        }

        // ============================
        // 6. DEPLOY
        // ============================
        stage('6. Production Deploy') {
            steps {

                sh "docker rm -f prod-site || true"

                sh """
                    docker run -d \
                    --name prod-site \
                    -p 8081:80 \
                    ${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG}
                """

                echo "========================================"
                echo " DEPLOYMENT SUCCESSFUL 🚀"
                echo " URL: http://localhost:8081"
                echo "========================================"
            }
        }
    }
}
