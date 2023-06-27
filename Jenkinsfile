pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'make stop'
                sh 'make build'
                sh 'make start'
            }
        }
        stage('Test') {
            steps {
                    sh 'docker exec erp-app pytest'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
