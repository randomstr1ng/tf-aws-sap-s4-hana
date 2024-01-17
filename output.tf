output "private_ip" {
  value = aws_instance.ec2_instance.private_ip
}

output "s4-hana_instance_id" {
  value = aws_instance.ec2_instance.id 
}