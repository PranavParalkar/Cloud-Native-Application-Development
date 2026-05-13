Architecture Overview 
Root Stack → VPC Stack (networking) + IAM Stack (roles/policies) + EC2 Stack (instance using VPC 
and IAM outputs) 
 
Step 1 – Upload Child Templates to S3 
All child templates must be stored in an S3 bucket before deployment. 
aws s3 mb s3://my-cfn-templates-bucket 
aws s3 cp vpc-stack.yaml    s3://my-cfn-templates-bucket/ 
aws s3 cp iam-stack.yaml    s3://my-cfn-templates-bucket/ 
aws s3 cp ec2-stack.yaml    s3://my-cfn-templates-bucket/

RUN

aws cloudformation create-stack --stack-name ExamRootStack --template-body file://root-stack.yaml --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey=TemplateBucket,ParameterValue=my-cfn-templates-bucket 

# Monitor events 
aws cloudformation describe-stack-events --stack-name ExamRootStack 

# Cleanup - deletes root and all nested stacks 
aws cloudformation delete-stack --stack-name ExamRootStack