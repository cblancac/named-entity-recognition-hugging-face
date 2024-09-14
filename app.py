import json
from pathlib import Path
import traceback
import json
import base64
import os
from datetime import datetime

import boto3

from cloud_service.cloud_service import AwsService
from entidades.engines.ner import (
    NerRegex,
    NerNeural,
)
from entidades.user_cases.entities_from_one_doc import entities_from_one_doc
from entidades.input_output.file_manager import SentencesFromPdfMiner


os.environ["TRANSFORMERS_CACHE"] = ".models/xlm-roberta-base-investing-ner"

BUCKET_NAME = "process-textract-python"
FOLDER_NAME = Path("tmp/")



s3_client = boto3.client("s3")

def handler(event, context):

    s3 = boto3.resource("s3")
    aws_service = AwsService(
        s3.Bucket(BUCKET_NAME),
        FOLDER_NAME,
    )
    message = "The File is Uploaded successfully!"
    try:
        params = event.get("queryStringParameters", {})
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%y%m%d-%H%M%S")

        default_filename = f"investing-{formatted_datetime}.pdf"
    
        filename_with_extension = params['filename'] if params is not None and "filename" in params else default_filename
        file_content = base64.b64decode(event['body'])
        
        uploadFile(file_content, filename_with_extension)
         
    except Exception as e: 
        message = str(e) 
        print(traceback.format_exc())
        
    reader_doc = SentencesFromPdfMiner()
    sentences = reader_doc.load_sentences_from_doc(filename_with_extension)
    ner_regex = NerRegex()
    ner_neural = NerNeural()

    entities = entities_from_one_doc(sentences, ner_regex, ner_neural)

    return {"statusCode": 200, "body": json.dumps(entities)}
    

def uploadFile(content, filenanme): 
    try:
        s3_upload = s3_client.put_object(Bucket=BUCKET_NAME ,Key=f"tmp/{filenanme}",Body=content) 
    except Exception as e:
        print("Error in Upload File :: ", e) 
        print(traceback.format_exc())
        raise e

