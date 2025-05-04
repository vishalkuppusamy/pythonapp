pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = 'kuppusav/pythonapp'
        SLACK_CHANNEL = '#jenkins'
        REGISTRY = 'docker.io'
        IMAGE_NAME = 'kuppusav/pythonapp'
        MANIFEST_REPO = 'https://github.com/vishalkuppusamy/pythonapp-k8s.git'
        SONARQUBE_SERVER = 'SonarQube-Server'
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
        stage('Trivy Scan') {
            steps {
                sh 'trivy image $DOCKER_HUB_REPO:${BUILD_NUMBER} || true'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'dockerhub', url: '']) {
                    sh 'docker push $DOCKER_HUB_REPO:${BUILD_NUMBER}'
                }
            }
        }
        stage('Update Kubernetes Manifest and Push') {
           steps {
    withCredentials([usernamePassword(credentialsId: 'github', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
        sh """
            git clone ${MANIFEST_REPO} pythonk8s-repo
            cd pythonk8s-repo
            sed -i 's|image:.*|image: ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}|' k8s-app.yaml
            git config user.email "kuppusav@gmail.com"
            git config user.name "kuppusav"
            git commit -am "Update image tag to ${BUILD_NUMBER}"
            git push https://$GIT_USERNAME:$GIT_PASSWORD@github.com/vishalkuppusamy/pythonapp-k8s.git main
        """
    }
}

        }
    }
    post {
        success {
            slackSend(channel: "${SLACK_CHANNEL}", message: "✅ *Pipeline Successful*: `${JOB_NAME}` build #${BUILD_NUMBER} (<${BUILD_URL}|View Build>)")
        }
        failure {
            slackSend(channel: "${SLACK_CHANNEL}", message: "🚨 *Pipeline Failed*: `${JOB_NAME}` build #${BUILD_NUMBER} (<${BUILD_URL}|View Build>)")
        }
        always {
            cleanWs()
        }
    }
}
