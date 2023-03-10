from pathlib import Path
import sys
from os import listdir
from os.path import isfile, join

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import boto3


if __name__ == "__main__":

    # Let's use Amazon S3
    s3 = boto3.client("s3")

    local_path_dataset = "data/preprocess/pdfs"
    bucket_name = "process-textract-python"
    folder_name = "upload-pdf"

    filenames = [f for f in listdir(local_path_dataset) if isfile(join(local_path_dataset, f))]

    for filename in filenames:
        print(filename)
        s3.upload_file(
            Filename=f"{local_path_dataset}/{filename}",
            Bucket=f"{bucket_name}",
            Key=f"{folder_name}/{filename}"
        )
