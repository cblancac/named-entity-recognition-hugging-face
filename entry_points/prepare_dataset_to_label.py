from pathlib import Path
import sys

import boto3

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from cloud_service.cloud_service import AwsService
from dataset.preprocess_files import PreprocessPDF
from split_document import SplitDocument
from utils.process_images import (
    ProcessImage,
)

s3 = boto3.resource("s3")
BUCKET_NAME = s3.Bucket("process-textract-python")
FOLDER_NAME = Path("upload-pdf")

OUTPUT_PATH = Path("data")
LOCAL_PATH_DATASET = Path("data/pdfs")
OUTPUT_PATH_DATASET = Path("data/ner_labels")

if __name__ == "__main__":
    # Upload pdf files to S3
    aws_service = AwsService(
        BUCKET_NAME,
        FOLDER_NAME,
        output_path=OUTPUT_PATH,
        local_path_dataset=LOCAL_PATH_DATASET,
    )
    #aws_service.upload_s3_dataset()

    # Call Textract service to get the response per pdf
    for object_summary in BUCKET_NAME.objects.filter(Prefix=f"{FOLDER_NAME}"):
        filename = object_summary.key

        response = aws_service.call_textract_service_dataset(filename)
        if not response:
            continue

        process_pdf = PreprocessPDF(response)
        grouped_words, grouped_coordinates = process_pdf.get_collections_grouped_by_pages()

        process_image = ProcessImage(filename)
        FILENAME = process_image.process_filename()
        images = process_image.convert_pdf_to_images(Path(LOCAL_PATH_DATASET) / f"{FILENAME}")
        size_images = process_image.get_size_per_image(images)

        split_doc = SplitDocument(
            grouped_words,
            grouped_coordinates,
            size_images
        )
        sentences = split_doc.split_doc_by_sentences()
        words = split_doc.split_doc_by_words(sentences)
        split_doc.export_datasets_splited(words, OUTPUT_PATH, FILENAME)
