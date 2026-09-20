pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }

    environment {
        APP_NAME = 'quality-gate-demo'
        COVERAGE_MIN = '80'
        PYTHON = 'C:\\Users\\Yasaswini\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
        VENV_PYTHON = '.venv\\Scripts\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment Setup') {
            steps {
                bat 'if not exist .venv "%PYTHON%" -m venv .venv'
                bat '%VENV_PYTHON% -m pip install --upgrade pip'
                bat '%VENV_PYTHON% -m pip install -r requirements.txt'
            }
        }

        stage('Validate Source') {
            steps {
                bat '%VENV_PYTHON% -m py_compile app\\*.py'
                bat '%VENV_PYTHON% -m flake8 app tests'
            }
        }

        stage('Automated Tests') {
            steps {
                bat 'if not exist reports mkdir reports'
                bat '%VENV_PYTHON% -m pytest tests --junitxml=reports\\junit.xml --cov=app --cov-report=xml:reports\\coverage.xml --cov-report=term --cov-fail-under=%COVERAGE_MIN%'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/junit.xml'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo "Quality gate passed: coverage >= ${env.COVERAGE_MIN}%"
            }
        }

        stage('Build') {
            steps {
                bat 'if not exist dist mkdir dist'
                bat 'powershell -Command "Compress-Archive -Path app -DestinationPath dist/%APP_NAME%-%BUILD_NUMBER%.zip -Force"'
            }
        }

        stage('Deployment Validation') {
            steps {
                bat '%VENV_PYTHON% scripts\\deployment_smoke_test.py'
            }
        }

        stage('Release Readiness') {
            steps {
                echo 'Release readiness checks passed.'
                echo 'Required gates: source validation, tests, coverage, build, deployment smoke test.'
            }
        }
    }

    post {
        success {
            echo "SUCCESS: ${env.APP_NAME} build ${env.BUILD_NUMBER} is release-ready."
        }
        failure {
            echo "FAILED: ${env.APP_NAME} build ${env.BUILD_NUMBER}. Release blocked."
        }
        always {
            archiveArtifacts artifacts: 'dist/*.zip, reports/*', allowEmptyArchive: true
        }
    }
}