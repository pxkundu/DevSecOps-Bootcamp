resource "aws_security_group" "jenkins_sg" {
  vpc_id = var.vpc_id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "jenkins" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
  instance_type = "t3.medium"
  key_name      = var.key_name
  subnet_id     = var.subnet_id
  security_groups = [aws_security_group.jenkins_sg.id]
  user_data     = file("../../../jenkins/setup-jenkins.sh")
  tags = {
    Name = "${var.env}-jenkins"
  }
}
