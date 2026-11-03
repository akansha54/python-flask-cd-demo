
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

        stage('Create Deployment Environment') {
            steps {
                echo 'Creating deployment Python environment'

                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "
                        $target = 'C:\\ProgramData\\Jenkins\\deployments\\Python-Flask-CD'
                        $venvPython = Join-Path $target '.venv\\Scripts\\python.exe'

                        if (!(Test-Path $venvPython)) {
                            python -m venv (Join-Path $target '.venv')
                        }

                        & $venvPython -m pip install -r (Join-Path $target 'requirements.txt')

                        if ($LASTEXITCODE -ne 0) {
                            exit $LASTEXITCODE
                        }
                    "
                '''
            }
        }
    }

    post {
        success {
            echo 'Flask CI and deployment preparation completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Please check the console output.'
        }
    }
}

