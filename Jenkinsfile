
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

        stage('Prepare Deployment') {
            steps {
                echo 'Preparing Flask application for deployment'

                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "
                        $target = 'C:\\ProgramData\\Jenkins\\deployments\\Python-Flask-CD'

                        New-Item -ItemType Directory -Force -Path $target | Out-Null

                        Copy-Item app.py, requirements.txt -Destination $target -Force

                        Copy-Item templates, static -Destination $target -Recurse -Force
                    "
                '''
            }
        }
    }

    post {
        success {
            echo 'Flask CI pipeline and deployment preparation completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Please check the console output.'
        }
    }
}
