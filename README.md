# SAP ABAP Platform Trial 
Terraform Module for SAP ABAP Platform Trial deployment on AWS Cloud.
This terraform deployment will setup a Ubuntu 22.04 EC2 Instance will allows to run the SAP ABAP Platform Trial.

On the EC2 Instance, Docker will be automatically installed. In addition, a script is provided which allows to refresh the licenses of the Container.

## How to use
```terraform
module "sap-s4hana" {
  source = "./modules/s4-hana"

  security_group_name = var.s4_hana_security_group_name
  ec2_name            = var.s4_hana_ec2_name
  vpc-id              = aws_vpc.vpc.id
  keypair-id          = aws_key_pair.key_pair.id
  subnet-id           = aws_subnet.subnet.id
}

# Output
output "sapcloudconnector_private_ip" {
  description = "SAP S/4HANA Instance Private IP"
  value = module.sap-s4hana.private_ip
}
```

## Links
- [DockerHub ABAP Platform Trial](https://hub.docker.com/r/sapse/abap-platform-trial)