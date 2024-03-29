variable "security_group_name" {
  type = string
  default = "s4hana_security_group"
}

variable "ec2_name" {
  type    = string
  default = "s4hana-vm"
}

variable "vpc-id" {
  type = string
}

variable "keypair-id" {
  type = string
}

variable "subnet-id" {
  type = string
}

variable "instance_type" {
  # min Requirements: 4vCPU, 16GB RAM, 150GB Disk
    type = string
    default = "t3.2xlarge"
}