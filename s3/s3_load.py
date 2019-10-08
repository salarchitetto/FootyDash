import os
import logging
import boto3
from botocore.exceptions import ClientError
from config import *

def upload_file(bucket, path, key, secret):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then same as file_name
    :return: True if file was uploaded, else False
    """

    s3_client = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=secret)

    for subdir, dirs, files in os.walk(path):
        print('Working on Directory: ' + str(subdir.split('\\')[-1:][0].title()))
        for file in files:
            # Upload the file
            try:
                response = s3_client.upload_file(os.path.join(subdir, file), bucket, str(file.split('.')[:1][0]))
            except ClientError as e:
                logging.error(e)
                print('An issue has occurred! ' + str(e))
                return False

    print('Files have been uploaded to S3!')

def get_s3_keys(bucket):
    """Get a list of keys in an S3 bucket."""
    keys = []
    client = boto3.client('s3', aws_access_key_id=KEY,
                          aws_secret_access_key=SECRET)
    resp = client.list_objects_v2(Bucket=bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys