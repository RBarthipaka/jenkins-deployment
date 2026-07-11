pipeline {
    agent any

    environment {
        APP_NAME     = "myapp"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                script {
                    // BRANCH_NAME is only auto-set in true Multibranch Pipeline jobs.
                    // Fall back to GIT_BRANCH (set by a plain checkout) so this also
                    // works correctly when run as a standalone Pipeline job.
                    def resolvedBranch = env.BRANCH_NAME ?: env.GIT_BRANCH
                    resolvedBranch = resolvedBranch ? resolvedBranch.replaceFirst('^origin/', '') : 'unknown'

                    env.RESOLVED_BRANCH = resolvedBranch
                    env.IMAGE_TAG   = "${APP_NAME}:${resolvedBranch}-${env.BUILD_NUMBER}"
                    env.LATEST_TAG  = "${APP_NAME}:${resolvedBranch}-latest"
                    env.CONTAINER   = "${APP_NAME}-${resolvedBranch}"
                    env.HOST_PORT   = (resolvedBranch == 'main' || resolvedBranch == 'master') ? '8501' : '8601'

                    echo "Resolved branch: ${resolvedBranch}, will deploy to port ${env.HOST_PORT}"
                }
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
                expression {
                    return env.RESOLVED_BRANCH in ['main', 'master', 'develop']
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
            echo "Build & deploy succeeded for branch ${env.RESOLVED_BRANCH} -> port ${env.HOST_PORT}"
        }
        failure {
            echo "Build failed for branch ${env.RESOLVED_BRANCH}. Check console log."
        }
        always {
            sh 'docker ps --filter "name=${APP_NAME}"'
        }
    }
}
