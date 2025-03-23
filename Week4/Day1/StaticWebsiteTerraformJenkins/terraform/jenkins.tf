resource "aws_vpc" "jenkins_vpc" {
  cidr_block = "10.1.0.0/16"
  tags = {
    Name = "JenkinsVPC"
  }
}

resource "aws_subnet" "jenkins_subnet" {
  vpc_id            = aws_vpc.jenkins_vpc.id
  cidr_block        = "10.1.1.0/24"
  map_public_ip_on_launch = true
  tags = {
    Name = "JenkinsSubnet"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.jenkins_vpc.id
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.jenkins_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public_rta" {
  subnet_id      = aws_subnet.jenkins_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_security_group" "jenkins_sg" {
  vpc_id = aws_vpc.jenkins_vpc.id
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
  tags = {
    Name = "JenkinsSG"
  }
}

resource "aws_instance" "jenkins" {
  ami                  = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
  instance_type        = "t3.medium"
  key_name             = var.key_name
  subnet_id            = aws_subnet.jenkins_subnet.id
  security_groups      = [aws_security_group.jenkins_sg.id]
  iam_instance_profile = aws_iam_instance_profile.jenkins_profile.name
  user_data            = file("../jenkins/setup-jenkins.sh")
  tags = {
    Name = "JenkinsServer"
  }
}