
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out Python Flask application'
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Pytest') {
            steps {
                bat 'python -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'All Flask application tests passed!'
        }

        failure {
            echo 'Pipeline failed. Please check the console output.'
        }
    }
}
