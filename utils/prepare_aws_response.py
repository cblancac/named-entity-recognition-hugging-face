import time

import boto3

textract = boto3.client('textract', region_name='eu-central-1')


def _start_job(bucket_name, document_name):
    response = None
    response = textract.start_document_text_detection(
    DocumentLocation={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': document_name
        }
    })

    return response["JobId"]


def _is_job_complete(jobId):
    response = textract.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = textract.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status


def _get_job_results(jobId):

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


def get_textract_response(bucket_name, filename):
    if filename.endswith(".pdf"):
        jobId = _start_job(bucket_name, filename)
        print("Started job with id: {}".format(jobId))
        if(_is_job_complete(jobId)):
            response = _get_job_results(jobId)
            return response
    return None