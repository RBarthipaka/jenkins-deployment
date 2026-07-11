pipeline {
    agent any

    environment {
        // Image name is tagged per branch so builds don't clash
        APP_NAME     = "myapp"
        IMAGE_TAG    = "${APP_NAME}:${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
        LATEST_TAG   = "${APP_NAME}:${env.BRANCH_NAME}-latest"
        CONTAINER    = "${APP_NAME}-${env.BRANCH_NAME}"
        // Only main/master gets deployed to the "real" port; other branches get a different port
        HOST_PORT    = "${env.BRANCH_NAME == 'main' ? '8501' : '8601'}"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${IMAGE_TAG} -t ${LATEST_TAG} .
                """
            }
        }

        stage('Test (optional)') {
            steps {
                sh '''
                    echo "Add pytest / lint commands here if you have tests"
                    # docker run --rm ${IMAGE_TAG} pytest
                '''
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                    branch 'develop'
                }
            }
            steps {
                sh """
                    # Stop and remove old container if it exists
                    docker stop ${CONTAINER} || true
                    docker rm ${CONTAINER} || true

                    # Run new container
                    docker run -d \\
                        --name ${CONTAINER} \\
                        --restart unless-stopped \\
                        -p ${HOST_PORT}:8501 \\
                        ${LATEST_TAG}
                """
            }
        }

        stage('Cleanup old images') {
            steps {
                sh '''
                    docker image prune -f
                '''
            }
        }
    }

    post {
        success {
            echo "Build & deploy succeeded for branch ${env.BRANCH_NAME} -> port ${HOST_PORT}"
        }
        failure {
            echo "Build failed for branch ${env.BRANCH_NAME}. Check console log."
        }
        always {
            sh 'docker ps --filter "name=${APP_NAME}"'
        }
    }
}
