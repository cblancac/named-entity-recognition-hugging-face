from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import boto3

from call_textract import CallTextract


if __name__ == "__main__":

    s3 = boto3.resource('s3')
    bucket_name = s3.Bucket('process-textract-python')
    output_path = "data/preprocess/txts"

    for object_summary in bucket_name.objects.filter(Prefix="upload-pdf/"):
        document_name = object_summary.key
        if document_name.endswith(".pdf"):
            textract_service = CallTextract(document_name, bucket_name.name)
            jobId = textract_service.start_job()
            print("Started job with id: {}".format(jobId))
            if(textract_service.is_job_complete(jobId)):
                response = textract_service.get_job_results(jobId)
                plain_text = textract_service.extract_plain_text(response)
                textract_service.save_text_plain(output_path, document_name, plain_text)