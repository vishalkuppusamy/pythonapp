pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = 'kuppusav/pythonapp'
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/vishalkuppusamy/pythonapp.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_HUB_REPO:${BUILD_NUMBER} .'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'dockerhub', url: '']) {
                    sh 'docker push $DOCKER_HUB_REPO:${BUILD_NUMBER}'
                }
            }
        }
    }
     post {
        success {
            echo 'Triggering another project: manifestk8s '
            build job: "manifestk8s", parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
        }
    }
}
