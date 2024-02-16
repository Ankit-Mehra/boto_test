"""
Upload a group of files to s3 bucket using boto3
Author : Ankit Mehra
"""

import boto3
import os
import sys
import logging
# import for timing the upload
import time

# Set the log level
logging.basicConfig(level=logging.INFO)

# Set the AWS credentials
class UploadFile:
    def __init__(self,local_folder):
        self.s3 = boto3.resource('s3')
        self.bucket_name = 'contentcen301154845.aws.ai'
        self.storage_location = 'assignment1/'
        self.local_folder = local_folder
    
    def upload_files(self)->None:
        """
        upload to s3 bucket from upload folder
        """
        try:
            for root, dirs, files in os.walk(self.local_folder):
                for file in files:
                    local_file = os.path.join(root, file)
                    print(local_file)
                    s3_file = os.path.join(self.storage_location, local_file)
                    self.s3.Bucket(self.bucket_name).upload_file(local_file, s3_file)
                    logging.info(f'File {local_file} uploaded to s3 bucket {self.bucket_name} at location {s3_file}')
        except Exception as e:
            logging.error(f'Error occured while uploading file to s3 bucket: {e}')
            sys.exit(1)
        logging.info('All files uploaded successfully to s3 bucket')

if __name__ == '__main__':
    time1 = time.time()
    upload = UploadFile('upload')
    upload.upload_files()
    time2 = time.time()
    print(f'Execution time: {time2-time1}')