#!groovy

node {
    registry_url = "https://index.docker.io/v1/"
    docker_creds_id = "1"
    build_tag = "testing"

    stage 'Git'
    git url: 'https://github.com/kinoreel/kinoreel-backend.git'

    stage 'testing'
    sh 'pip install -r requirements.txt'
    sh 'sh test.sh'

    stage 'Push Docker'
    docker.withRegistry("${registry_url}", "${docker_creds_id}") {
        maintainer_name = "kinoreel"
        container_name = "backend"
        stage "Building"
        echo "Building the docker container"
        container = docker.build("${maintainer_name}/${container_name}:${build_tag}", '.')
        stage "Pushing"
        container.push()

        currentBuild.result = 'SUCCESS'
    }
}