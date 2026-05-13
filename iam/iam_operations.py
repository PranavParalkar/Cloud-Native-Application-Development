import boto3
import json

iam = boto3.client('iam')

# Create User
response = iam.create_user(UserName='exam-user')
print("User created:", response['User']['UserName'])

# Create Access Key
keys = iam.create_access_key(UserName='exam-user')

print("Access Key ID:", keys['AccessKey']['AccessKeyId'])
print("Secret Key:", keys['AccessKey']['SecretAccessKey'])

# Create Group
iam.create_group(GroupName='DevGroup')

# Add User to Group
iam.add_user_to_group(
    GroupName='DevGroup',
    UserName='exam-user'
)

print("User added to group")

# Attach Policy
iam.attach_group_policy(
    GroupName='DevGroup',
    PolicyArn='arn:aws:iam::aws:policy/ReadOnlyAccess'
)

print("Policy attached")

# Trust Policy
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {
            "Service": "ec2.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
    }]
}

# Create Role
role = iam.create_role(
    RoleName='EC2AdminRole',
    AssumeRolePolicyDocument=json.dumps(trust_policy),
    Description='Role for EC2 admin access'
)

print("Role created:", role['Role']['Arn'])

# Attach Role Policy
iam.attach_role_policy(
    RoleName='EC2AdminRole',
    PolicyArn='arn:aws:iam::aws:policy/AmazonEC2FullAccess'
)

print("Role policy attached")

# Custom Inline Policy
custom_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "s3:GetObject",
            "s3:PutObject"
        ],
        "Resource": "arn:aws:s3:::my-bucket/*"
    }]
}

iam.put_user_policy(
    UserName='exam-user',
    PolicyName='S3CustomAccess',
    PolicyDocument=json.dumps(custom_policy)
)

print("Inline policy added")

# List Users
users = iam.list_users()

print("\nUsers:")
for u in users['Users']:
    print(u['UserName'])

# Cleanup
iam.detach_group_policy(
    GroupName='DevGroup',
    PolicyArn='arn:aws:iam::aws:policy/ReadOnlyAccess'
)

iam.remove_user_from_group(
    GroupName='DevGroup',
    UserName='exam-user'
)

iam.delete_group(GroupName='DevGroup')

iam.delete_access_key(
    UserName='exam-user',
    AccessKeyId=keys['AccessKey']['AccessKeyId']
)

iam.delete_user_policy(
    UserName='exam-user',
    PolicyName='S3CustomAccess'
)

iam.delete_user(UserName='exam-user')

print("\nCleanup complete")