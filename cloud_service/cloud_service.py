from abc import ABC, abstractmethod
from os import listdir
from os.path import isfile, join

import boto3
from tqdm import tqdm
from colorama import Fore, init

from utils.prepare_aws_response import get_textract_response
from utils.save_response import save_response_json, save_text_plain

init(autoreset=True)
s3 = boto3.client("s3")


class CloudService(ABC):
    """Class representing a cloud service"""

    @abstractmethod
    def call_textract_service_dataset(self, filename) -> None:
        """Extract information from files"""

    @abstractmethod
    def upload_s3_dataset(self) -> None:
        """Upload dataset to Cloud"""

    def upload_s3_file(self, filename) -> None:
        """Upload file to Cloud"""


class AwsService(CloudService):
    """Class representing a AWS service"""

    def __init__(
        self,
        bucket_name: str,
        folder_name: str,
        output_path: str = "",
        local_path_dataset: str = "",
    ):
        self.bucket_name = bucket_name
        self.folder_name = folder_name
        self.output_path = output_path
        self.local_path_dataset = local_path_dataset

    def call_textract_service_dataset(self, filename) -> None:
        response = get_textract_response(self.bucket_name.name, filename)
        save_response_json(response, self.output_path, filename)
        save_text_plain(response, self.output_path, filename)
        return response

    def upload_s3_file(self, filename) -> None:
        s3.upload_file(
            Filename=f"{self.local_path_dataset}/{filename}",
            Bucket=f"{self.bucket_name}",
            Key=f"{self.folder_name}/{filename}",
        )

    def upload_s3_dataset(self) -> None:
        filenames = [
            f
            for f in listdir(self.local_path_dataset)
            if isfile(join(self.local_path_dataset, f))
        ]
        for filename in tqdm(filenames):
            self.upload_s3_file(filename)
            print(f"{filename} {Fore.YELLOW} [Uploading file...]")
        print(f"{Fore.GREEN} [All files have been uploaded correctly]")
