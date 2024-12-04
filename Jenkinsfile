pipeline {
    agent any
    environment {
        FLASK_ENV = 'test'
        DATABASE_URL = 'postgresql://sonar:sonar@db:5432/flask_db'
        SONARQUBE_ENV = 'SonarQube'
    }
    stages {

        stage('Checkout Repository') {
            steps {
                git branch: 'lab4', url: 'https://github.com/murickg/pdris_lab3.git'
            }
        }

        stage('Updating system') {
            steps {
                sh 'apt-get update'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'apt install -y python3 python3-pip'
                sh 'apt install -y python3-pytest python3-venv'
                sh 'apt install -y libpq-dev'
                sh 'apt install allure-pytest'
            }
        }
        stage("Build Virtual Environment"){
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip3 install --upgrade pip
                    pip3 install -r app/requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest test/app_test.py --cov=app --junitxml=test-results.xml --cov-report=xml:coverage_results.xml --alluredir=allure-results
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                    ])
                }
            }
        }
        stage('Code Analysis') {
            environment {
                scannerHome = tool 'sonar'
            }
            steps {
                script {
                    withSonarQubeEnv('sonar') {
                        sh '''
                        ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=pdris-lab4 \
                            -Dsonar.projectName="pdris lab4" \
                            -Dsonar.projectVersion=1.0 \
                            -Dsonar.sources=app/ \
                            -Dsonar.language=py \
                            -Dsonar.host.url=http://sonarqube:9000 \
                            -Dsonar.python.coverage.reportPaths=coverage_results.xml \
                            -Dsonar.login=$SONAR_AUTH_TOKEN
                        '''
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Something wrong with pipeline!'
        }
    }
}