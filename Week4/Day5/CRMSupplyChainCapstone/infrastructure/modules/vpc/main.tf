resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  tags = { Name = "crm-supply-vpc" }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 1)
  availability_zone = "${var.region}a"
  tags = { Name = "private-subnet-${count.index}" }
}
