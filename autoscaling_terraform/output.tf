# outputs.tf 
output "alb_dns_name" {
  value       = aws_lb.main.dns_name
  description = "ALB DNS - open this in browser to test"
}