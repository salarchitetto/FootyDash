import boto3
import pandas as pd
import psycopg2
from config import *
from sql_queries.create_tables import staging_copy

def get_redshiftcluster_host(redshift, cluster_identifier):
    """

    :param redshift:
    :param cluster_identifier:
    :return:
    """

    props = redshift.describe_clusters(ClusterIdentifier=cluster_identifier)['Clusters'][0]
    keysToShow = ["Endpoint"]
    x = [(k, v) for k, v in props.items() if k in keysToShow]

    return x[0][1]['Address']

def redshift_connection(host, dbname, user, password, port=5439):
    """
    Connection to redshift database
    :param host:
    :param dbname:
    :param user:
    :param password:
    :param port:
    :return:
    """

    global conn, cur
    try:
        conn = psycopg2.connect(
            f"host={host} dbname={dbname} user={user} password={password} port={port}")
        cur = conn.cursor()
    except Exception as e:
        print('Failue to upload: ' + str(e))

    return conn, cur


def upload_to_redshift(paths, key, secret, roleArn, conn, cur):
    """

    :param paths:
    :param key:
    :param secret:
    :return:
    """
    client = boto3.client('s3', aws_access_key_id=key,
                          aws_secret_access_key=secret)

    for x in paths:
        print(x)

        obj = client.get_object(Bucket=BUCKET_NAME, Key=x)
        df = pd.read_csv(obj['Body'])

        lst = list(df.columns)
        lst = [x for x in lst if '<' not in x and '>' not in x]
        lst = ','.join(lst)
        lst = '(' + lst + ')'
        print(lst)
        print(staging_copy.format(lst, x ,roleArn))

        try:
            cur.execute(staging_copy.format(lst, x ,roleArn))
            conn.commit()
        except Exception as e:
            print('Failue to upload: ' + str(e))
