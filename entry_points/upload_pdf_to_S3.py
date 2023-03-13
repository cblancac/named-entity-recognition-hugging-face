from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from aws_service.aws_uploader import AwsUploader

if __name__ == "__main__":

    bucket_name = "process-textract-python"
    folder_name = "upload-pdf"
    local_path_dataset = "data/preprocess/pdfs"

    s3_service = AwsUploader(bucket_name, folder_name, local_path_dataset)
    s3_service.upload_S3_dataset()
