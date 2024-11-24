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
                pytest test/app_test.py --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
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