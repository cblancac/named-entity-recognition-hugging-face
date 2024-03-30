from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Tuple

import boto3
from pdfminer.high_level import extract_text
import pytesseract

from dataset.preprocess_files import PreprocessPDF
from dataset.split_document import SplitDocument
from utils.process_images import (
    ProcessImage,
)
from cloud_service.cloud_service import AwsService
from utils.prepare_aws_response import get_textract_response
from utils.process_images import convert_from_bytes
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
    def load_sentences_from_doc(self, path: str) -> List[str]:
        raise NotImplementedError
    
class SentencesFromPdfMiner(FileManager):
    def load_sentences_from_doc(self, path: str) -> str:
        return extract_text(str(LOCAL_PATH_DATASET / path))
    
class SentencesFromTextract(FileManager):
    def load_sentences_from_doc(self, path: str) -> str:
        self._upload_file_s3(path)
        response = get_textract_response(aws_service.bucket_name.name, str(FOLDER_NAME / path))
        
        process_pdf = PreprocessPDF(response)
        grouped_words, grouped_coordinates = process_pdf.get_collections_grouped_by_pages()

        split_doc = SplitDocument(
            grouped_words,
            grouped_coordinates,
            self._get_size_images(path)
        )
        
        sentences = split_doc.split_doc_by_sentences()
        sentences = [sentence['text'] for sentence in sentences]
        return sentences
        #return extract_plain_text(response)
    
    def _upload_file_s3(self, path: str) -> None:
        # Upload pdf file to S3
        aws_service.upload_s3_file(str(path))

    def _get_object(self, path):
        obj = s3.Object(aws_service.bucket_name.name, str(FOLDER_NAME / path))
        archivoBase64 = obj.get()['Body'].read()
        return archivoBase64
    
    def _get_size_images(self, path):
        process_image = ProcessImage(path)
        images = process_image.convert_pdf_to_images(self._get_object(path))
        size_images = process_image.get_size_per_image(images)
        return size_images

class SentencesFromPytesseract(FileManager):
    def load_sentences_from_doc(self, path: str) -> str:
        images = convert_from_bytes(str(LOCAL_PATH_DATASET / path))
        return self._concat_text_from_images(images)

    def _concat_text_from_images(self, images):
        text = ""
        for image in images:
            text = text + " " + pytesseract.image_to_string(image)
        return text


