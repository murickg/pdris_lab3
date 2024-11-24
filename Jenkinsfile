pipeline {
    agent any
    environment {
        FLASK_ENV = 'test'             // Окружение для Flask
        DATABASE_URL = 'postgresql://sonar:sonar@db:5432/flask_db' // URL базы данных
        SONARQUBE_ENV = 'SonarQube'       // Имя настроенного SonarQube сервера
    }
    stages {

        stage('Checkout Repository') {
            steps {
                git branch: 'lab4', url: 'https://github.com/murickg/pdris_lab3.git'
            }
        }

//         stage('Debugging') {
//             steps {
//                 sh '''
//                     echo "Current working directory:"
//                     pwd
//                     echo "Listing all files:"
//                     ls -R
//                 '''
//             }
//         }

        stage('Updating system') {
            steps {
                sh 'apt-get update'
            }
        }

        stage('Install Dependencies') {
            steps {
                // установка зависимостей для сборки
                sh 'apt install -y python3 python3-pip'
                // Установка зависимостей для тестов
                sh 'apt install -y python3-pytest python3-venv'
            }
        }
        stage("Build Virtual Environment"){
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip3 install --upgrade pip
                    pip3 install -r ./lab4/DB/app/requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                // Запуск тестов и генерация отчёта покрытия
                sh '''
                source venv/bin/activate
                pytest ./test --junitxml=test-results.xml
                '''
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