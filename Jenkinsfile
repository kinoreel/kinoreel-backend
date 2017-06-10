#!groovy

node {
    registry_url = "https://index.docker.io/v1/"
    docker_creds_id = "1"
    build_tag = "latest"

    stage 'Git'
    git url: 'https://github.com/kinoreel/kinoreel-backend.git'

    stage 'testing'
    sh 'pip install --user -r requirements.txt'
    sh 'sh test.sh'

    docker.withRegistry("${registry_url}", "${docker_creds_id}") {
        maintainer_name = "kinoreel"
        container_name = "backend"
        stage "Building Docker image"
        echo "Building the docker image"
        container = docker.build("${maintainer_name}/${container_name}:${build_tag}", '.')
        stage "Pushing Docker image"
        container.push()

        currentBuild.result = 'SUCCESS'
    }
    stage 'Deploy application'
    milestone()
    input message: "Proceed?"
    milestone()
    sh 'cd charts; sh deploy.sh'
}