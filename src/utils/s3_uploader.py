import os
import boto3
from botocore.exceptions import NoCredentialsError

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "driver-drowsiness-storage")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def upload_file_to_s3(file_path, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)
    try:
        s3_client.upload_file(file_path, S3_BUCKET_NAME, object_name)
        print(f" Successfully uploaded {object_name} to AWS S3 Bucket: {S3_BUCKET_NAME}")
        return f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{object_name}"
    except NoCredentialsError:
        print(" AWS Credentials missing or invalid.")
        return None
    except Exception as e:
        print(f" Failed to upload to S3: {e}")
        return None
