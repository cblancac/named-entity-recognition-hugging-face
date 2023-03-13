from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import boto3

from aws_service.aws_textract import AwsTextract

if __name__ == "__main__":

    s3 = boto3.resource('s3')
    bucket_name = s3.Bucket('process-textract-python')
    folder_name = "upload-pdf/"    
    out_path_json = "data/preprocess/json"
    out_path_text = "data/preprocess/txts"

    textract_service = AwsTextract(bucket_name, folder_name, out_path_json, out_path_text)
    textract_service.call_textract_service_dataset()