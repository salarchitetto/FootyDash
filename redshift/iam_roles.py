import pandas as pd
import boto3
from botocore.exceptions import ClientError
import json

def connect_iam(key, secret):
    """
    makes a connection to iam user using aws creds
    """

    iam = boto3.client('iam', aws_access_key_id=key,
                        aws_secret_access_key=secret
                        )
    return iam

def create_iam_role(iam, iam_role_name):
    """
    This creates an IAM Role for our redshift cluster
    """

    try:
        print("Creating a new IAM Role")
        user = iam.create_role(
            Path='/',
            RoleName=iam_role_name,
            Description="Connect to Redshift, Create Redshift, Connect S3, Create S3.",
            AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                                'Effect': 'Allow',
                                'Principal': {'Service': 'redshift.amazonaws.com'}}],
                 'Version': '2012-10-17'})
        )
    except Exception as e:
        print(e)

def add_roles(iam, iam_role_name):
    """
    We need specific permissions for us to actually user the data
    so here they are.
    """

    roles = ['AmazonRedshiftFullAccess', 'AmazonRedshiftQueryEditor',
             'AmazonS3FullAccess', 'AdministratorAccess']

    for x in roles:
        iam.attach_role_policy(RoleName=iam_role_name,
                               PolicyArn=f"arn:aws:iam::aws:policy/{x}")['ResponseMetadata']['HTTPStatusCode']

def grab_iam_creds(iam, iam_role_name):
    """
    grab the iam role arn to use for creating the redshift cluster
    """

    roleArn = iam.get_role(RoleName=iam_role_name)['Role']['Arn']

    return roleArn