import os
import boto3
import threading
from botocore.exceptions import NoCredentialsError

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "driver-drowsiness-storage")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

s3_client = None

def _get_s3_client():
    global s3_client
    if s3_client is None:
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        if access_key and secret_key:
            try:
                s3_client = boto3.client(
                    "s3",
                    region_name=AWS_REGION,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key
                )
            except Exception as e:
                print(f"S3 Client init error: {e}")
    return s3_client

def _do_upload(file_path, object_name):
    client = _get_s3_client()
    if not client:
        return
    try:
        client.upload_file(file_path, S3_BUCKET_NAME, object_name)
        print(f" Successfully uploaded {object_name} to AWS S3 Bucket: {S3_BUCKET_NAME}")
    except Exception as e:
        print(f" Failed to upload to S3: {e}")

def upload_file_to_s3(file_path, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)
    # Launch upload in background thread so Flask API request never blocks or lags
    threading.Thread(target=_do_upload, args=(file_path, object_name), daemon=True).start()
    return True
