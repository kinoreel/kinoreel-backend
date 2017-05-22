#!groovy
@Library('github.com/lachie83/jenkins-pipeline@master')
def pipeline = new io.estrado.Pipeline()

podTemplate(label: 'jenkins-pipeline', containers: [
    containerTemplate(name: 'helm', image: 'lachlanevenson/k8s-helm:v2.4.1', command: 'cat', ttyEnabled: true)
]){

node {
    registry_url = "https://index.docker.io/v1/"
    docker_creds_id = "1"
    build_tag = "latest"

    stage 'Git'
    git url: 'https://github.com/kinoreel/kinoreel-backend.git'

    stage 'testing'
    sh 'pip install --user -r requirements.txt'
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
    stage ('Helm install') {

      container('helm') {

        // run helm chart linter
        pipeline.helmLint(chart_dir)

        // run dry-run helm chart installation
        pipeline.helmDeploy(
          dry_run       : true,
          name          : "kino-backend",
          version_tag   : "0.1",
          chart_dir     : chart_dir,
          replicas      : "3",
          cpu           : "10m",
          memory        : "128Mi"
        )

      }
    }
}
}