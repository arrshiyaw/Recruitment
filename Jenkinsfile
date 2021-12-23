 pipeline {
    agent {
        docker { image 'python:3.6-alpine' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'python contact/APITest.py'
            }
        }
    }
}