pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout([$class: 'GitSCM',
                    userRemoteConfigs: [[
                        url: 'https://github.com/vishalkuppusamy/pythonapp.git',
                        credentialsId: 'github'
                    ]],
                    branches: [[name: '*/main']]
                ])
            }
        }

        stage('Docker') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub', // corrected key
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )])
            }
        }
    }

    post {
        always {
            echo 'Pipeline was completed.'
        }
        success {
            echo 'Pipeline was successful.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
