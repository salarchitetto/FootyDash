import os
from scraper.csv_download import *
from s3.s3_create import create_bucket
from s3.s3_load import upload_file,  get_s3_keys
from s3.data_clean import add_division_names, create_seasons, choose_columns, rename_file
from redshift.create_redshift import aws_redshift, create_redshift_cluster, check_redshift_status
from redshift.iam_roles import connect_iam, create_iam_role, add_roles, grab_iam_creds
from redshift.load_redshift import upload_to_redshift, get_redshiftcluster_host, redshift_connection
from sql_queries.create_tables import  drop_table_queries, create_table_queries
from sql_queries.insert_tables import insert_queries
from config import *
import psycopg2
import time
import warnings
warnings.filterwarnings("ignore")

def drop_tables(cur, conn):
    """
    Drops tables in the warehouse
    """

    for query in drop_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    """
    Loops through and runs the create statements
    """

    for query in create_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()

def insert_tables(cur,conn):
    """
    Loops through and runs the insert statements
    """

    for query in insert_queries:
        print(query)
        cur.execute(query)
        conn.commit()

if __name__ == '__main__':
    print('*' * 50)
    try:
        os.mkdir(file_path + 'footy_data_sets')
        file_path = file_path  + 'footy_data_sets'
        create_directory(file_path, list_of_links)
    except Exception as e:
        ValueError('Directory already exists. ' + str(e))

    print('Working on downloading the data for the individual countries')
    print('*' * 50)

    grab_uk_data()
    grab_scot_data()
    grab_germany_data()
    grab_italy_data()
    grab_spain_data()
    grab_france_data()
    grab_netherlands_data()
    grab_belgium_data()
    grab_portugal_data()
    print('Completed the CSV downloads!')
    print('*' * 50)

    print('Cleaning up the CSVs, should take a quick second.')
    time.sleep(5)

    print('creating seasons columns')
    create_seasons(s3_path)
    print('*' * 50)
    # print('creating divisions column')
    add_division_names(s3_path)
    print('*' * 50)
    choose_columns(s3_path)
    print('Changing some CSV names')
    rename_file(s3_path)
    print('Creating the S3 bucket via your Amazon Credentials')
    create_bucket(BUCKET_NAME, KEY, SECRET)

    print('*' * 50)
    print('Uploading data into: ' + str(BUCKET_NAME))
    upload_file(BUCKET_NAME, s3_path, KEY, SECRET)
    print('*' * 50)

    print('*' * 50)
    print('Connecting to iam via AWS')
    iam = connect_iam(KEY, SECRET)

    print('Creating IAM role')
    create_iam_role(iam, IAM_ROLE_NAME)
    print('Adding some roles to the user')
    add_roles(iam, IAM_ROLE_NAME)
    print('Snagging the credentials')
    roleArn = grab_iam_creds(iam, IAM_ROLE_NAME)
    print('*' * 50)

    print('Connecting to Redshift via AWS')
    redshift = aws_redshift(KEY,SECRET)
    print('Creating the Redshift Cluster!')
    create_redshift_cluster(redshift, REDSHIFT_USERNAME, REDSHIFT_PASSWORD, roleArn, DB_NAME, CLUSTER_IDENTIFIER)
    print('Waiting on the redshift cluster to become available')

    while True:
        ready = check_redshift_status(redshift, CLUSTER_IDENTIFIER)
        if ready == 'available':
            print('Redshift Cluster is now available!')
            break

    print('*' * 50)
    print('Lets Create some tables!')
    print('Uploading the staging data')

    paths = get_s3_keys(BUCKET_NAME)
    redshift_host = get_redshiftcluster_host(redshift, CLUSTER_IDENTIFIER)
    redshift_conn, redshift_cur = redshift_connection(redshift_host, DB_NAME,REDSHIFT_USERNAME, REDSHIFT_PASSWORD)
    print('Dropping some tables.. if they somehow exists...')
    drop_tables(redshift_cur, redshift_conn)
    print('Creating some tables')
    create_tables(redshift_cur, redshift_conn)
    print('UPLOADING FOOTY DATA TO REDSHIFT CLUSTER')
    upload_to_redshift(paths, KEY, SECRET,roleArn, redshift_conn, redshift_cur)
    print('Loading up the rest of the tables')
    insert_tables(redshift_cur, redshift_conn)
    print('*' * 50)
    print('DONE: Everything is all set. Enjoy the data!')