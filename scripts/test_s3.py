
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

bucket_name = os.getenv("S3_BUCKET_NAME")
region = os.getenv("AWS_DEFAULT_REGION")

s3 = boto3.client(
    "s3",
    region_name=region
)

try:
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        MaxKeys=10
    )

    print("AWS S3 CONNECTION SUCCESSFUL!")
    print("\nFiles in your bucket:")

    for obj in response.get("Contents", []):
        print(obj["Key"])

except Exception as e:
    print("AWS CONNECTION FAILED!")
    print(e)
