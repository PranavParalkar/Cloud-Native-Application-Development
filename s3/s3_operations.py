import boto3
import json

# Use Mumbai region
s3 = boto3.client('s3', region_name='ap-south-1')

BUCKET = 'my-exam-bucket-cnda-1'

# For ap-south-1, CreateBucketConfiguration is REQUIRED
s3.create_bucket(
    Bucket=BUCKET,
    CreateBucketConfiguration={
        'LocationConstraint': 'ap-south-1'
    }
)

print('Bucket created:', BUCKET)

# Enable Versioning
s3.put_bucket_versioning(
    Bucket=BUCKET,
    VersioningConfiguration={'Status': 'Enabled'}
)

print('Versioning enabled.')

# Upload local file
s3.upload_file(
    'local_file.txt',
    BUCKET,
    'uploads/local_file.txt'
)

# Upload from string content
s3.put_object(
    Bucket=BUCKET,
    Key='hello.txt',
    Body=b'Hello from Boto3!',
    ContentType='text/plain'
)

print('File uploaded.')

# List objects
response = s3.list_objects_v2(Bucket=BUCKET)

if 'Contents' in response:

    for obj in response['Contents']:

        print(
            obj['Key'],
            '|',
            obj['Size'],
            'bytes'
        )

else:
    print('Bucket is empty.')

# Download object
s3.download_file(
    BUCKET,
    'hello.txt',
    'downloaded_hello.txt'
)

print('File downloaded.')

# Read object directly
obj = s3.get_object(
    Bucket=BUCKET,
    Key='hello.txt'
)

content = obj['Body'].read().decode('utf-8')

print('Content:', content)

# Generate pre-signed URL
url = s3.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': BUCKET,
        'Key': 'hello.txt'
    },
    ExpiresIn=3600
)

print('Pre-signed URL:', url)

# Enable static website hosting
s3.put_bucket_website(
    Bucket=BUCKET,
    WebsiteConfiguration={
        'IndexDocument': {'Suffix': 'index.html'},
        'ErrorDocument': {'Key': 'error.html'}
    }
)

print('Static website hosting enabled.')

# Bucket policy
policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'PublicReadGetObject',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': 's3:GetObject',
        'Resource': f'arn:aws:s3:::{BUCKET}/*'
    }]
}

# Disable Block Public Access

s3.put_public_access_block(
    Bucket=BUCKET,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': False,
        'IgnorePublicAcls': False,
        'BlockPublicPolicy': False,
        'RestrictPublicBuckets': False
    }
)

print("Public access block disabled.")

s3.put_bucket_policy(
    Bucket=BUCKET,
    Policy=json.dumps(policy)
)

print('Bucket policy applied.')

# Cleanup Section

# Delete all objects first
# response = s3.list_objects_v2(Bucket=BUCKET)

# if 'Contents' in response:

#     objects = [
#         {'Key': o['Key']}
#         for o in response['Contents']
#     ]

#     s3.delete_objects(
#         Bucket=BUCKET,
#         Delete={'Objects': objects}
#     )

# Delete bucket
# s3.delete_bucket(Bucket=BUCKET)

# print('Bucket deleted.')