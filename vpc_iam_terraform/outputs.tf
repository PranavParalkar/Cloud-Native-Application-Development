# outputs.tf
output "vpc_id" {
	value = aws_vpc.main.id
}

output "public_subnet" {
	value = aws_subnet.public.id
}

output "bucket_name" {
	value = aws_s3_bucket.main.id
}

output "ec2_role_arn" {
	value = aws_iam_role.ec2_role.arn
}

output "dev_user_name" {
	value = aws_iam_user.dev_user.name
}