 pipeline {
    agent {
        docker { dockerfile true }
    }
    stages {
        stage('Test') {
            steps {
                sh 'python contact/APITest.py'
            }
        }
    }
}