import pandas as pd
import boto3
from botocore.exceptions import ClientError
from redshift.iam_roles import create_iam_role, grab_iam_creds
import json


def redshift_connect(key, secret):
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

    :return:
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

    :param redshift:
    :param cluster_identifier:
    :return:
    """

    props = redshift.describe_clusters(ClusterIdentifier=cluster_identifier)['Clusters'][0]

    keysToShow = ["ClusterStatus"]
    x = [(k, v) for k,v in props.items() if k in keysToShow]

    while True:
        if x[0][1] == 'available':
            print('Redshift cluster is now available!')
            return True
        else:
            continue


