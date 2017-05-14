pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                /* `make check` returns non-zero on test failures,
                * using `true` to allow the Pipeline to continue nonetheless
                */
                sh 'pip install -r requirements.txt'
                sh 'sh test.sh'
            }
        }
        stage('Push Docker') {
            steps{
                def app = docker.build 'kinoreel/backend:0.0.1'
                app.push
            }
        }
    }
}