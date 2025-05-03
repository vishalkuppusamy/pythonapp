pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = 'kuppusav/pythonapp'
        SLACK_CHANNEL = '#pragrajenkins'
        REGISTRY = 'docker.io'
        IMAGE_NAME = 'kuppusav/pythonapp'
        ARGO_REPO = 'git@github.com:vishalkuppusamy/pythonapp-k8s.git'
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/vishalkuppusamy/pythonapp.git'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    sh 'sonar-scanner -Dsonar.projectKey=pythonapp -Dsonar.sources=.'
                }
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
                sshagent (credentials: ['argo-repo-ssh-key']) {
                    sh '''
                        git clone ${ARGO_REPO} argo-repo
                        cd argo-repo
                        sed -i "s|image:.*|image: ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}|" manifests/deployment.yaml
                        git config user.email "ci@company.com"
                        git config user.name "CI Bot"
                        git commit -am "Update image tag to ${BUILD_NUMBER}"
                        git push origin main
                    '''
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
