import os
from scraper.csv_download import *
from s3.s3_create import create_bucket
from s3.s3_load import upload_file

from config import *
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':

    try:
        os.mkdir(file_path + 'footy_data_sets')
        file_path = file_path  + 'footy_data_sets'
        create_directory(file_path, list_of_links)
    except Exception as e:
        ValueError('Directory already exists. ' + str(e))

    print('Working on downloading the data for the individual countries')

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

    print('Creating the S3 bucket via your Amazon Credentials')
    create_bucket(BUCKET_NAME, KEY, SECRET)

    print('Uploading data into: ' + str(BUCKET_NAME))
    upload_file(BUCKET_NAME, s3_path, KEY, SECRET)

