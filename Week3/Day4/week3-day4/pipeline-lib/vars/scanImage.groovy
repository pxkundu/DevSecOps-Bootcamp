def call(String imageName) {
    sh "docker run --rm aquasec/trivy image --severity HIGH,CRITICAL ${imageName}"
}
