resource "aws_security_group" "security_group" {
  name        = var.security_group_name
  description = var.security_group_name
  vpc_id      = var.vpc-id

  ingress {
    from_port   = 22
    protocol    = "tcp"
    to_port     = 22
    description = "SSH access"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3200
    protocol    = "tcp"
    to_port     = 3200
    description = "SAPGUI Instance 00"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3300
    protocol    = "tcp"
    to_port     = 3300
    description = "RFC Instance 00"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 30213
    protocol    = "tcp"
    to_port     = 30213
    description = "SAP HANA MDC Database"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 50000
    protocol    = "tcp"
    to_port     = 50000
    description = "AS ABAP HTTP"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 50001
    protocol    = "tcp"
    to_port     = 50001
    description = "AS ABAP HTTPS"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 50013
    protocol    = "tcp"
    to_port     = 50013
    description = "SAP Start Service HTTP Instance 00"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 50014
    protocol    = "tcp"
    to_port     = 50014
    description = "SAP Start Service HTTPS Instance 00"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 50113
    protocol    = "tcp"
    to_port     = 50113
    description = "SAP Start Service HTTP Instance 01"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 50114
    protocol    = "tcp"
    to_port     = 50114
    description = "SAP Start Service HTTPS Instance 01"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 50213
    protocol    = "tcp"
    to_port     = 50213
    description = "SAP Start Service HTTP Instance 02"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 50214
    protocol    = "tcp"
    to_port     = 50214
    description = "SAP Start Service HTTPS Instance 02"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name  = "architecture"
    values = ["x86_64"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "ec2_instance" {
# min Requirements: 4vCPU, 16GB RAM, 150GB Disk
  instance_type          = "t3.2xlarge"
  ami                    = data.aws_ami.ubuntu.id
  key_name               = var.keypair-id
  vpc_security_group_ids = [aws_security_group.security_group.id]
  subnet_id              = var.subnet-id
  user_data              = base64encode(templatefile("${path.module}/bootstrap.tftpl", {})) 

  tags = {
    Name = var.ec2_name
  }

  root_block_device {
    volume_size = 150
  }
}