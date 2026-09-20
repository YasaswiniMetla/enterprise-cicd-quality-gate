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
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Source') {
            steps {
                bat 'python -m py_compile app/*.py'
                bat 'python -m flake8 app tests'
            }
        }

        stage('Automated Tests') {
            steps {
                bat 'if not exist reports mkdir reports'
                bat 'python -m pytest tests --junitxml=reports/junit.xml --cov=app --cov-report=xml:reports/coverage.xml --cov-report=term --cov-fail-under=%COVERAGE_MIN%'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/junit.xml'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    if (currentBuild.currentResult == 'FAILURE') {
                        error('Quality gate failed. Build cannot proceed.')
                    }
                }
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
                bat 'python scripts/deployment_smoke_test.py'
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
