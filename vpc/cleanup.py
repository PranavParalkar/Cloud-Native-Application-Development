import boto3

print("Starting cleanup...")

ec2 = boto3.client('ec2', region_name='ap-south-1')

# Find all VPCs with CIDR 10.0.0.0/16
vpcs = ec2.describe_vpcs()

target_vpcs = []

for vpc in vpcs['Vpcs']:
    if vpc['CidrBlock'] == '10.0.0.0/16':
        target_vpcs.append(vpc['VpcId'])

if not target_vpcs:
    print("No matching VPCs found.")
    exit()

for vpc_id in target_vpcs:

    print(f"\nCleaning VPC: {vpc_id}")

    # -----------------------------
    # Delete Security Groups
    # -----------------------------
    sgs = ec2.describe_security_groups(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [vpc_id]
            }
        ]
    )

    for sg in sgs['SecurityGroups']:

        if sg['GroupName'] != 'default':

            try:
                ec2.delete_security_group(
                    GroupId=sg['GroupId']
                )

                print("Deleted SG:", sg['GroupId'])

            except Exception as e:
                print("SG Error:", e)

    # -----------------------------
    # Route Tables
    # -----------------------------
    rts = ec2.describe_route_tables(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [vpc_id]
            }
        ]
    )

    for rt in rts['RouteTables']:

        for assoc in rt.get('Associations', []):

            if not assoc.get('Main', False):

                try:
                    ec2.disassociate_route_table(
                        AssociationId=assoc['RouteTableAssociationId']
                    )

                    print("Disassociated Route Table")

                except Exception as e:
                    print("Disassociation Error:", e)

        is_main = any(
            assoc.get('Main', False)
            for assoc in rt.get('Associations', [])
        )

        if not is_main:

            try:
                ec2.delete_route_table(
                    RouteTableId=rt['RouteTableId']
                )

                print("Deleted Route Table")

            except Exception as e:
                print("RT Error:", e)

    # -----------------------------
    # Internet Gateway
    # -----------------------------
    igws = ec2.describe_internet_gateways(
        Filters=[
            {
                'Name': 'attachment.vpc-id',
                'Values': [vpc_id]
            }
        ]
    )

    for igw in igws['InternetGateways']:

        igw_id = igw['InternetGatewayId']

        try:
            ec2.detach_internet_gateway(
                InternetGatewayId=igw_id,
                VpcId=vpc_id
            )

            ec2.delete_internet_gateway(
                InternetGatewayId=igw_id
            )

            print("Deleted IGW:", igw_id)

        except Exception as e:
            print("IGW Error:", e)

    # -----------------------------
    # Delete Subnets
    # -----------------------------
    subnets = ec2.describe_subnets(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [vpc_id]
            }
        ]
    )

    for subnet in subnets['Subnets']:

        try:
            ec2.delete_subnet(
                SubnetId=subnet['SubnetId']
            )

            print("Deleted Subnet:", subnet['SubnetId'])

        except Exception as e:
            print("Subnet Error:", e)

    # -----------------------------
    # Delete VPC
    # -----------------------------
    try:
        ec2.delete_vpc(VpcId=vpc_id)

        print("Deleted VPC:", vpc_id)

    except Exception as e:
        print("VPC Error:", e)

print("\nCleanup completed.")