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