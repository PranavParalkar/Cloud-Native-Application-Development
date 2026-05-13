# variables.tf 
variable "aws_region" {
	default = "ap-south-1"
}

variable "project" {
	default = "exam-asg"
}

variable "instance_type" {
	default = "t2.micro"
}

variable "min_size" {
	default = 2
}

variable "max_size" {
	default = 5
}

variable "desired_cap" {
	default = 2
}