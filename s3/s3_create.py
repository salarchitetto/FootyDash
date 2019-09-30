import logging
import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name, key, secret, region = None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    try:
        if region is None:
            s3_client = boto3.client('s3', aws_access_key_id = key, aws_secret_access_key = secret)
            s3_client.create_bucket(Bucket = bucket_name)
        else:
            s3_client = boto3.client('s3',aws_access_key_id = key, aws_secret_access_key = secret,
                                     region_name = region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket = bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        print('Looks like something went wrong! ' + str(e))

    print(('Bucket:' + str(bucket_name) + ' has been created!'))

