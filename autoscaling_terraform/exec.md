# Deploy 
terraform init 
terraform plan 
terraform apply -auto-approve 
  
# Test 
curl http://$(terraform output -raw alb_dns_name) 
  
# Destroy 
terraform destroy -auto-approve 