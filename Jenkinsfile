#!groovy

node {
    registry_url = "https://index.docker.io/v1/"
    docker_creds_id = "1"
    build_tag = "latest"

    stage 'Git'
    git url: 'https://github.com/kinoreel/kinoreel-backend.git'

    docker.withRegistry("${registry_url}", "${docker_creds_id}") {
        maintainer_name = "kinoreel"
        container_name = "backend"
        stage "Building Docker image"
        echo "Building the docker image"
        image = "${maintainer_name}/${container_name}:${build_tag}"
        container = docker.build("${image}", " --build-arg PG_SERVER=${env.PG_SERVER} --build-arg PG_PORT=${env.PG_PORT} --build-arg PG_DB=${env.PG_DB} --build-arg PG_USERNAME=${env.PG_USERNAME} --build-arg PG_PASSWORD=${env.PG_PASSWORD} .")

        stage 'Testing docker'
        sh """docker run -it --entrypoint="sh test.sh" ${image}"""
        container.inside {
          sh 'sh test.sh'
        }

        stage "Pushing Docker image"
        container.push()

        currentBuild.result = 'SUCCESS'
    }
    stage 'Clean docker image'
    sh 'docker rmi kinoreel/backend'
    echo "${env.BRANCH_NAME}"
    if ("${env.BRANCH_NAME}" == "master")
    {
        stage 'Deploy application'
        milestone()
        input message: "Proceed?"
        milestone()
        sh 'cd charts; sh deploy.sh'
    }
}