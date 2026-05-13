import boto3

print("Starting VPC setup in ap-south-1...")

# Create EC2 client for Mumbai region
ec2 = boto3.client('ec2', region_name='ap-south-1')

# -----------------------------
# Create VPC
# -----------------------------
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc['Vpc']['VpcId']

print("VPC ID:", vpc_id)

# Enable DNS
ec2.modify_vpc_attribute(
    VpcId=vpc_id,
    EnableDnsHostnames={'Value': True}
)

ec2.modify_vpc_attribute(
    VpcId=vpc_id,
    EnableDnsSupport={'Value': True}
)

# -----------------------------
# Create Public Subnet
# -----------------------------
pub_subnet = ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='10.0.1.0/24',
    AvailabilityZone='ap-south-1a'
)

pub_subnet_id = pub_subnet['Subnet']['SubnetId']

# -----------------------------
# Create Private Subnet
# -----------------------------
priv_subnet = ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='10.0.2.0/24',
    AvailabilityZone='ap-south-1b'
)

priv_subnet_id = priv_subnet['Subnet']['SubnetId']

print("Public Subnet:", pub_subnet_id)
print("Private Subnet:", priv_subnet_id)

# -----------------------------
# Create Internet Gateway
# -----------------------------
igw = ec2.create_internet_gateway()
igw_id = igw['InternetGateway']['InternetGatewayId']

ec2.attach_internet_gateway(
    InternetGatewayId=igw_id,
    VpcId=vpc_id
)

print("Internet Gateway attached:", igw_id)

# -----------------------------
# Create Route Table
# -----------------------------
rt = ec2.create_route_table(VpcId=vpc_id)
rt_id = rt['RouteTable']['RouteTableId']

# Add route to Internet
ec2.create_route(
    RouteTableId=rt_id,
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=igw_id
)

# Associate Route Table with Public Subnet
ec2.associate_route_table(
    RouteTableId=rt_id,
    SubnetId=pub_subnet_id
)

print("Route table configured and associated.")

# -----------------------------
# Create Security Group
# -----------------------------
sg = ec2.create_security_group(
    GroupName='WebServerSG',
    Description='Allow HTTP and SSH',
    VpcId=vpc_id
)

sg_id = sg['GroupId']

# Allow SSH and HTTP inbound
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

print("Security Group created:", sg_id)

# -----------------------------
# Add Tags
# -----------------------------
resources = [
    vpc_id,
    pub_subnet_id,
    priv_subnet_id,
    igw_id,
    rt_id,
    sg_id
]

for rid in resources:
    ec2.create_tags(
        Resources=[rid],
        Tags=[
            {
                'Key': 'Project',
                'Value': 'ExamVPC'
            }
        ]
    )

print("Tags applied to all resources.")

# -----------------------------
# Verify Resources
# -----------------------------
vpcs = ec2.describe_vpcs(VpcIds=[vpc_id])

print("VPC State:", vpcs['Vpcs'][0]['State'])

subnets = ec2.describe_subnets(
    Filters=[
        {
            'Name': 'vpc-id',
            'Values': [vpc_id]
        }
    ]
)

for s in subnets['Subnets']:
    print("Subnet:", s['SubnetId'], "|", s['CidrBlock'])

print("\nVPC setup completed successfully.")

