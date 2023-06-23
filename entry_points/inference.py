from pathlib import Path
import sys

import boto3

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from cloud_service.cloud_service import AwsService
from entidades.user_cases.entities_from_one_doc import entities_from_one_doc
from entidades.engines.ner import (
    NerRegex,
    NerNeural,
)
from utils.save_response import extract_plain_text

s3 = boto3.resource("s3")
BUCKET_NAME = s3.Bucket("process-textract-python")
FOLDER_NAME = Path("upload-pdf")

OUTPUT_PATH = Path("data")
LOCAL_PATH_DATASET = Path("data/pdfs")
OUTPUT_PATH_DATASET = Path("data/ner_labels")

if __name__ == "__main__":
    FILENAME = "6 big dividends_ Jackson Financial hikes, Saratoga keeps jumbo yield _ Pro Recap By Investing.com.pdf"

    # Upload pdf file to S3
    aws_service = AwsService(
        BUCKET_NAME,
        FOLDER_NAME,
        output_path=OUTPUT_PATH,
        local_path_dataset=LOCAL_PATH_DATASET,
    )

    aws_service.upload_s3_file(FILENAME)
    response = aws_service.call_textract_service(str(FOLDER_NAME / FILENAME))
    text = extract_plain_text(response)
    ner_regex = NerRegex()
    ner_neural = NerNeural()

    entities = entities_from_one_doc(text, ner_regex, ner_neural)
    print(entities)
