def call(String logFile, String streamName) {
    withAWS(credentials: 'aws-creds', region: 'us-east-1') {
        sh "aws logs put-log-events --log-group-name JenkinsLogs --log-stream-name ${streamName}-${BUILD_NUMBER} --log-events file:///${logFile}"
    }
}
