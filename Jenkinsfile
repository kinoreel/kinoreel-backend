pipeline {
    agent any
    registry_url = "https://index.docker.io/v1/"
    docker_creds_id = "1"
    build_tag = "testing"

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
                docker.withRegistry("${registry_url}", "${docker_creds_id}") {
                    maintainer_name = "kinoreel"
                    container_name = "backend"
                    stage "Building"
                    echo "Building the docker container"
                    container = docker.build("${maintainer_name}/${container_name}:${build_tag}", 'django')
                    stage "Pushing"
                    container.push()

                    currentBuild.result = 'SUCCESS'
                }
            }
        }
    }
}