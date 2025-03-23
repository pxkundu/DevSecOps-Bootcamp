### `README.md`

# Jenkins Master-Slave Automation Project

This project automates the deployment of a Jenkins master-slave architecture on AWS using Amazon Linux 2. It leverages AWS CloudFormation to create a secure, scalable CI/CD environment integrated with Amazon ECR and GitHub.

## Project Structure

- `templates/jenkins-master-slave.yaml`: CloudFormation template for infrastructure.
- `deploy.sh`: Script to validate and deploy the stack.
- `lifecycle/ecr-lifecycle.json`: ECR lifecycle policy to manage image retention.
- `scripts/`: Placeholder for initialization scripts.
- `config/`: Placeholder for Jenkins configuration files.
- `tests/`: Placeholder for validation scripts.
- `.gitignore`: Ignores `.pem` and `.log` files.

## Prerequisites

- **AWS Account**: Configured with AWS CLI (`aws configure`).
- **EC2 Key Pair**: Created in `us-east-1` (e.g., `my-key`).
- **Secrets Manager**: Store your GitHub SSH private key as `github-ssh-key`.
- **ECR Repository**: `partha-ecr` in `us-east-1`.

## Setup Instructions

1. **Clone or Generate the Project**
   - If using the script:
     ```bash
     chmod +x create-jenkins-project.sh
     ./create-jenkins-project.sh
     cd JenkinsMasterSlaveAutomation
     ```
   - Or clone from your Git repo if hosted.

2. **Customize the Deployment Script**
   - Edit `deploy.sh`:
     - Replace `<your-key-name>` with your EC2 key pair name (e.g., `my-key`).
   - Verify the AMI in `templates/jenkins-master-slave.yaml` (`ami-0c55b159cbfafe1f0`) matches Amazon Linux 2 in your region.

3. **Deploy the Stack**
   ```bash
   ./deploy.sh
   ```
   - Wait 10-15 minutes for the stack to complete.
   - Check status: `aws cloudformation describe-stacks --stack-name JenkinsMasterSlave --region us-east-1`.

4. **Post-Deployment Configuration**
   - **Access Jenkins**:
     - URL: `http://<MasterPublicIP>:8080` (from stack outputs).
     - Initial Password: SSH into master and run:
       ```bash
       ssh -i <key>.pem ec2-user@<MasterPublicIP> "sudo cat /var/lib/jenkins/secrets/initialAdminPassword"
       ```
   - **Configure Slave**:
     - In Jenkins UI: `Manage Jenkins > Manage Nodes > New Node`.
     - Name: `slave1`, Label: `slave`, Launch Method: `Launch agent via Java Web Start`.
     - Copy the secret, then SSH into the slave and update:
       ```bash
       ssh -i <key>.pem ec2-user@<SlavePublicIP>
       pkill java
       cd /home/ec2-user/jenkins
       java -jar agent.jar -jnlpUrl http://<MasterPrivateIP>:8080/computer/slave1/jenkins-agent.jnlp -secret <secret> -workDir /home/ec2-user/jenkins &
       ```

5. **Apply ECR Lifecycle Policy**
   ```bash
   aws ecr put-lifecycle-policy --repository-name partha-ecr --lifecycle-policy-text file://lifecycle/ecr-lifecycle.json --region us-east-1
   ```

## Usage

- **Create a Pipeline**:
  - Add your `Jenkinsfile.functions` to `git@github.com:pxkundu/JenkinsTask.git`.
  - In Jenkins UI: `New Item > Pipeline`, point to your repo, and run.
- **Verify**:
  - Check builds run on `slave`.
  - Access app: `curl http://<SlavePublicIP>/`.

## Cleanup

- Delete the stack:
  ```bash
  aws cloudformation delete-stack --stack-name JenkinsMasterSlave --region us-east-1
  ```

## Notes

- Replace `<MasterPublicIP>`, `<SlavePublicIP>`, and `<MasterPrivateIP>` with values from stack outputs.
- Secure the master by restricting Security Group ingress (e.g., your IP instead of `0.0.0.0/0`).
- Extend with plugins or scripts in `scripts/` and `config/` as needed.

---
Created: March 16, 2025
---
