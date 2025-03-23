resource "aws_db_instance" "rds" {
  identifier           = "crm-supply-db"
  engine              = "postgres"
  instance_class      = var.instance_class
  allocated_storage   = 20
  db_name             = var.db_name
  username            = "admin"
  password            = "securepassword"  # Replace in production with secrets management
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  backup_retention_period = 7
  skip_final_snapshot    = true
}

resource "aws_security_group" "rds_sg" {
  vpc_id = var.vpc_id
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # Restrict to VPC CIDR
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = var.subnet_ids
}
