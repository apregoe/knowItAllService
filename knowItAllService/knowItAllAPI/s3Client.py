import boto3
from botocore.client import Config
from .constants import *

def saveFile(bucketName, path, fileName, fileBinary):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=Config(signature_version='s3v4')
    )

    bucket = s3.Bucket(bucket_name)
    bucket.put_object(
        Key=path+fileName,
        Body = fileBinary
    )