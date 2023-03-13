from os import listdir
from os.path import isfile, join

import boto3

from aws_service.aws_manager import AwsManager


s3 = boto3.client("s3")


class AwsUploader(AwsManager):
    def __init__(self, bucket_name, folder_name, local_path_dataset):
        AwsManager.__init__(self, bucket_name, folder_name)
        self.local_path_dataset = local_path_dataset

    def upload_S3_dataset(self):
        filenames = [f for f in listdir(self.local_path_dataset) if isfile(join(self.local_path_dataset, f))]
        for filename in filenames:
            print(filename)
            self.upload_s3_file(filename)

    def upload_s3_file(self, filename):
        s3.upload_file(
            Filename=f"{self.local_path_dataset}/{filename}",
            Bucket=f"{self.bucket_name}",
            Key=f"{self.folder_name}/{filename}"
        ) 