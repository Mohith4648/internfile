pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = "mohith4648"
        // ENTER YOUR REAL DOCKER HUB PASSWORD HERE
        DOCKER_HUB_PASS = "your_real_password_here" 
        
        IMAGE_NAME = "intern-project"
        TAG = "v1"
    }

    stages {
        stage('1. Setup & Workspace Cleanup') {
            steps {
                // Ensures a fresh start every time
                cleanWs()
                git branch: 'main', url: 'https://github.com/Mohith4648/internfile.git'
            }
        }

        stage('2. Docker Image Build') {
            steps {
                dir('UI') {
                    echo "Starting Docker Build for ${env.IMAGE_NAME}..."
                    sh "docker build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG} ."
                }
            }
        }

        stage('3. Selenium Quality Gate') {
            steps {
                script {
                    // 1. PRE-CLEANUP: Kill any lingering test containers from previous builds
                    sh "docker rm -f test-con || true"
                    
                    // 2. START TEST ENVIRONMENT
                    sh "docker run -d --name test-con -p 8085:80 ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                    
                    try {
                        echo "Running Selenium Automation Suite..."
                        // 3. EXECUTE TESTS: Using a containerized Python environment
                        // This ensures the test runs regardless of Jenkins server limitations
                        sh """
                            docker run --rm \
                            --network host \
                            -v ${WORKSPACE}/UI/tests:/apps \
                            -w /apps \
                            python:3.9-slim /bin/sh -c "pip install --no-cache-dir selenium && python selenium_check.py"
                        """
                        echo "SELENIUM VERIFICATION PASSED"
                    } catch (Exception e) {
                        echo "SELENIUM VERIFICATION FAILED: ${e.getMessage()}"
                        // Hard fail: This ensures the build STOPS if tests fail
                        error "Build aborted due to Selenium test failures. Quality Gate not met."
                    } finally {
                        // 4. POST-CLEANUP: Always stop the test container
                        sh "docker rm -f test-con || true"
                    }
                }
            }
        }

        stage('4. Security Login & Push') {
            steps {
                echo "Pushing verified image to Docker Hub..."
                sh """
                    echo "${env.DOCKER_HUB_PASS}" | docker login -u "${env.DOCKER_HUB_USER}" --password-stdin
                    docker push ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}
                    docker logout
                """
            }
        }

        stage('5. Production Deployment') {
            steps {
                echo "Deploying to Production Environment..."
                // Ensure production container is updated cleanly
                sh "docker rm -f prod-site || true"
                sh "docker run -d --name prod-site -p 8081:80 ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.TAG}"
                
                echo "------------------------------------------------------------"
                echo " PROJECT SUBMISSION READY"
                echo " Status: DEPLOYED"
                echo " URL: http://localhost:8081"
                echo "------------------------------------------------------------"
            }
        }
    }
}
