def call(String imageName, String dir, String region) {
    dir(dir) {
        sh "docker build --cache-from <account-id>.dkr.ecr.${region}.amazonaws.com/${imageName}:latest -t ${imageName} ."
        withAWS(credentials: 'aws-creds', region: region) {
            sh "aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.${region}.amazonaws.com"
            sh "docker tag ${imageName} <account-id>.dkr.ecr.${region}.amazonaws.com/${imageName}"
            sh "docker push <account-id>.dkr.ecr.${region}.amazonaws.com/${imageName}"
            sh "aws s3 cp Dockerfile s3://<your-bucket>/artifacts/${imageName.split(':')[0]}-${BUILD_NUMBER}/"
        }
    }
}
