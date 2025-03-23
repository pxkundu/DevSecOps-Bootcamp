def call(String imageName, String instanceTag, String previousImage) {
    withAWS(credentials: 'aws-creds', region: 'us-east-1') {
        def instanceIp = sh(script: "aws ec2 describe-instances --filters Name=tag:Name,Values=${instanceTag} Name=instance-state-name,Values=running --query 'Reservations[0].Instances[0].PublicIpAddress' --output text", returnStdout: true).trim()
        try {
            sh "ssh -i ~/.ssh/jenkins_master_key -o StrictHostKeyChecking=no ec2-user@${instanceIp} 'docker stop ${imageName.split(':')[0]} || true'"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'docker rm ${imageName.split(':')[0]} || true'"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com'"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'docker pull <account-id>.dkr.ecr.us-east-1.amazonaws.com/${imageName}'"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'docker run -d --name ${imageName.split(':')[0]} -p ${imageName.contains('backend') ? '3000:3000' : '8080:8080'} <account-id>.dkr.ecr.us-east-1.amazonaws.com/${imageName}'"
        } catch (Exception e) {
            echo "Deploy failed, rolling back to ${previousImage}"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'docker stop ${imageName.split(':')[0]} || true'"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'docker rm ${imageName.split(':')[0]} || true'"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'docker pull <account-id>.dkr.ecr.us-east-1.amazonaws.com/${previousImage}'"
            sh "ssh -i ~/.ssh/jenkins_master_key ec2-user@${instanceIp} 'docker run -d --name ${imageName.split(':')[0]} -p ${imageName.contains('backend') ? '3000:3000' : '8080:8080'} <account-id>.dkr.ecr.us-east-1.amazonaws.com/${previousImage}'"
            throw e
        }
    }
}
