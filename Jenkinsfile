pipeline {
    agent any

    environment {
        IMAGE_NAME = 'kuppusav/pythonapp'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code...'
                checkout([
                    $class: 'GitSCM',
                    userRemoteConfigs: [[
                        url: 'https://github.com/vishalkuppusamy/pythonapp.git',
                        credentialsId: 'github'
                    ]],
                    branches: [[name: '*/main']]
                ])
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                echo 'Logging in and pushing image...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker build -t $IMAGE_NAME .
                        docker push $IMAGE_NAME
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Image pushed to Docker Hub successfully.'
        }
        failure {
            echo 'Pipeline failed. Check error logs.'
        }
    }
}
