import os
from scraper.csv_download import *
from s3.s3_create import create_bucket
from s3.s3_load import upload_file
from s3.data_clean import divisions_column, add_division_names, create_seasons
from redshift.create_redshift import redshift_connect, create_redshift_cluster, check_redshift_status
from redshift.iam_roles import connect_iam, create_iam_role, add_roles, grab_iam_creds
from config import *
import warnings
warnings.filterwarnings("ignore")

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
    time.sleep(10)

    print('creating seasons columns')
    create_seasons(s3_path)
    print('*' * 50)
    # print('creating divisions column')
    add_division_names(s3_path)
    print('*' * 50)

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
    redshift = redshift_connect(KEY,SECRET)
    print('Creating the Redshift Cluster!')
    create_redshift_cluster(redshift, REDSHIFT_USERNAME, REDSHIFT_PASSWORD, roleArn, DB_NAME, CLUSTER_IDENTIFIER)
    print('Waiting on the redshift cluster to become available')
    check_redshift_status(redshift, CLUSTER_IDENTIFIER)

