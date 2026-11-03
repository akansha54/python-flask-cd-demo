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
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$target='C:\\ProgramData\\Jenkins\\deployments\\Python-Flask-CD'; New-Item -ItemType Directory -Force -Path $target | Out-Null; Copy-Item app.py, requirements.txt -Destination $target -Force; Copy-Item templates, static -Destination $target -Recurse -Force; Write-Host 'Application files copied successfully'"
                '''
            }
        }

        stage('Create Deployment Environment') {
            steps {
                echo 'Creating deployment Python environment'

                bat '''
                    if not exist "C:\\ProgramData\\Jenkins\\deployments\\Python-Flask-CD\\.venv\\Scripts\\python.exe" python -m venv "C:\\ProgramData\\Jenkins\\deployments\\Python-Flask-CD\\.venv"

                    "C:\\ProgramData\\Jenkins\\deployments\\Python-Flask-CD\\.venv\\Scripts\\python.exe" -m pip install -r "C:\\ProgramData\\Jenkins\\deployments\\Python-Flask-CD\\requirements.txt"

                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Start Flask Application') {
            steps {
                echo 'Starting deployed Flask application'

                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$target='C:\\ProgramData\\Jenkins\\deployments\\Python-Flask-CD'; $waitress=Join-Path $target '.venv\\Scripts\\waitress-serve.exe'; if (!(Test-Path $waitress)) { throw 'Waitress executable not found' }; $processes=Get-NetTCPConnection -LocalPort 5001 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; foreach ($listenerProcessId in $processes) { Stop-Process -Id $listenerProcessId -Force }; Start-Sleep -Seconds 2; Start-Process -FilePath $waitress -ArgumentList '--listen=127.0.0.1:5001','app:app' -WorkingDirectory $target -WindowStyle Hidden -RedirectStandardOutput (Join-Path $target 'app.log') -RedirectStandardError (Join-Path $target 'error.log'); Write-Host 'Flask application startup initiated'"
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Verifying deployed Flask application'

                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ready=$false; for ($i=0; $i -lt 15; $i++) { try { $response=Invoke-WebRequest 'http://127.0.0.1:5001/' -UseBasicParsing; if ($response.StatusCode -eq 200) { $ready=$true; break } } catch { Start-Sleep -Seconds 2 } }; if (!$ready) { throw 'Deployment verification failed. Check error.log' }; Write-Host 'SUCCESS: Flask application is running on port 5001'"
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: CI and CD pipeline completed!'
            echo 'Flask application deployed and verified.'
        }

        failure {
            echo 'FAILED: Please check Jenkins Console Output.'
        }
    }
}
