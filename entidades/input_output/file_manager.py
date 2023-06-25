from abc import ABC, abstractmethod
from pathlib import Path

import boto3
from pdfminer.high_level import extract_text
import pytesseract

from cloud_service.cloud_service import AwsService
from utils.prepare_aws_response import get_textract_response
from utils.process_images import convert_from_path
from utils.save_response import extract_plain_text


s3 = boto3.resource("s3")
BUCKET_NAME = s3.Bucket("process-textract-python")
FOLDER_NAME = Path("upload-pdf")

OUTPUT_PATH = Path("data")
LOCAL_PATH_DATASET = Path("data/pdfs")
OUTPUT_PATH_DATASET = Path("data/ner_labels")

aws_service = AwsService(
    BUCKET_NAME,
    FOLDER_NAME,
    output_path=OUTPUT_PATH,
    local_path_dataset=LOCAL_PATH_DATASET,
)


class FileManager(ABC):
    @abstractmethod
    def load_info_from_doc(self, path: str) -> str:
        """dinie"""
        raise NotImplementedError
    
class TxtFromPdfMiner(FileManager):
    def load_info_from_doc(self, path: str) -> str:
        return extract_text(str(LOCAL_PATH_DATASET / path))
    
class TxtFromTextract(FileManager):
    def load_info_from_doc(self, path: str) -> str:
        self._upload_file_s3(path)
        response = get_textract_response(aws_service.bucket_name.name, str(FOLDER_NAME / path))
        return extract_plain_text(response)
    
    def _upload_file_s3(self, path: str) -> None:
        # Upload pdf file to S3
        aws_service.upload_s3_file(str(path))

class TxtFromPytesseract(FileManager):
    def load_info_from_doc(self, path: str) -> str:
        images = convert_from_path(str(LOCAL_PATH_DATASET / path))
        return self._concat_text_from_images(images)


    def _concat_text_from_images(self, images):
        text = ""
        for image in images:
            text = text + " " + pytesseract.image_to_string(image)
        return text


