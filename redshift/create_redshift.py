import pandas as pd
import boto3
from botocore.exceptions import ClientError
from redshift.iam_roles import create_iam_role, grab_iam_creds
import json


def aws_redshift(key, secret):
    """
    connect to redshift
    """

    redshift = boto3.client('redshift',
                            region_name="us-east-2",
                            aws_access_key_id=key,
                            aws_secret_access_key=secret
                            )
    return redshift

def create_redshift_cluster(redshift, awsuser, password, iamRole,
                            dbname, identifier):
    """
    This function essentially creates the redshift cluster
    with the parameters in the config file
    """

    try:
        response = redshift.create_cluster(
            # HW
            ClusterType='multi-node',
            NodeType='dc2.large',
            NumberOfNodes=int(4),

            # Identifiers & Credentials
            DBName=dbname,
            ClusterIdentifier=identifier,
            MasterUsername=awsuser,
            MasterUserPassword=password,

            # Roles (for s3 access)
            IamRoles=[iamRole]
        )

    except ClientError as e:
        print(f'ERROR: {e}')
        return None
    else:
        return response['Cluster']

def check_redshift_status(redshift, cluster_identifier):
    """
    This checks to see if the cluster is actually available
    This is used in run.py in a while loop - once available it
    breaks the loop
    """

    props = redshift.describe_clusters(ClusterIdentifier=cluster_identifier)['Clusters'][0]

    keysToShow = ["ClusterStatus"]
    x = [(k, v) for k,v in props.items() if k in keysToShow]

    return x[0][1]



