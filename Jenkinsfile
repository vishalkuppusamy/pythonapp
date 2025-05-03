pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = 'kuppusav/pythonapp'
        SLACK_CHANNEL = '#pragrajenkins'
        REGISTRY = 'docker.io'
        IMAGE_NAME = 'kuppusav/pythonapp'
        MANIFEST_REPO = 'git@github.com:vishalkuppusamy/pythonapp-k8s.git'
        SONARQUBE_SERVER = 'SonarQube-Server'
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/vishalkuppusamy/pythonapp.git'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectKey=pythonappkey \
                        -Dsonar.projectName=pythonapp \
                        -Dsonar.sources=. \
                        -Dsonar.language=py \
                        -Dsonar.inclusions=**/*.py \
                        -Dsonar.host.url=http://159.203.53.52:9000 \
                        -Dsonar.login=sqp_17308c0d9cd588aaff935a58a91b01caa85b9808
                        """
                }
         }
    }
}
    

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
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
                sshagent (credentials: ['k8s-repo-ssh-key']) {
                    sh '''
                        git clone ${MANIFEST_REPO} pythonk8s-repo
                        cd pythonk8s-repo
                        sed -i "s|image:.*|image: ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}|" manifests/deployment.yaml
                        git config user.email "kuppusav@gmail.com"'
                        git config user.name "kuppusav"
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
