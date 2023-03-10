import os
import time

import boto3


textract = boto3.client('textract', region_name='eu-west-1')


class CallTextract():
    def __init__(self, document_name, bucket_name):
        self.document_name = document_name 
        self.bucket_name   = bucket_name 

    def start_job(self):
        response = None
        response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': self.bucket_name,
                'Name': self.document_name
            }
        })

        return response["JobId"]

    def is_job_complete(self, jobId):
        response = textract.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

        while(status == "IN_PROGRESS"):
            time.sleep(5)
            response = textract.get_document_text_detection(JobId=jobId)
            status = response["JobStatus"]
            print("Job status: {}".format(status))

        return status

    def get_job_results(self, jobId):

        pages = []
        response = textract.get_document_text_detection(JobId=jobId)

        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']

        while(nextToken):
            response = textract.get_document_text_detection(JobId=jobId, NextToken=nextToken)

            pages.append(response)
            print("Resultset page recieved: {}".format(len(pages)))
            nextToken = None
            if('NextToken' in response):
                nextToken = response['NextToken']

        return pages
    
    def extract_plain_text(self, response):
        text_plain = ""
        for i in range(len(response)):
            for block in response[i]['Blocks']:
                if block["BlockType"] == "WORD":
                    text_plain = text_plain + " " + block["Text"]
        text_plain = text_plain.strip()
        return text_plain

    def _preprocess_filename(self, filename):
        filename = '/'.join(filename.split("/")[1:])
        return f"{filename[:-4]}.txt"
    
    def save_text_plain(self, output_path, filename, text_plain):
        filename = self._preprocess_filename(filename)

        exist_path = os.path.exists(output_path)
        if not exist_path:
            os.makedirs(output_path)
   
        text_file = open(f"{output_path}/{filename}", "w")
        text_file.write(text_plain)
        print(f"Text extracted from document {filename} and saved correctly!")
        text_file.close()



