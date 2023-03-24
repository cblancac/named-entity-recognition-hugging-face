from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from aws_service.aws_textract import AwsTextract
from aws_service.aws_uploader import AwsUploader
from split_document import SplitDocument
from utils.get_words_and_coord_per_pages import (
    get_collection_of_words_coords_pages,
    get_collections_grouped_by_pages,
)
from utils.prepare_aws_response import (
    get_textract_response
)
from utils.process_images import (
    get_size_per_image,
    convert_pdf_to_images
)


if __name__ == "__main__":

    # Upload pdf files to S3
    bucket_name = "process-textract-python"
    folder_name = "upload-pdf"
    local_path_dataset = "data/preprocess/pdfs"

    out_path_json = "data/preprocess/json"
    out_path_text = "data/preprocess/txts"

    s3_service = AwsUploader(bucket_name, folder_name, local_path_dataset)
    s3_service.upload_S3_dataset()

    # Call Textract service to get the response per pdf
    textract_service = AwsTextract(bucket_name, folder_name, out_path_json, out_path_text)
    for object_summary in bucket_name.objects.filter(Prefix=f"{folder_name}"):
        filename = object_summary.key

        response = get_textract_response(filename=filename)

        #Get the list of words, coordinates and pages
        list_words, list_coordinates, list_pages = get_collection_of_words_coords_pages(response)

        # Get the list of words, coordinates and pages per pages
        grouped_words, grouped_coordinates = get_collections_grouped_by_pages(list_words,
                                                                              list_coordinates,
                                                                              list_pages)
        
        images = convert_pdf_to_images(f"{local_path_dataset}/{filename}")
        size_images = get_size_per_image(images)

    
    





    local_path_pdfs = "data/preprocess/pdfs"
    local_path_json = "data/preprocess/json"
    output_path = "data/preprocess/ner_labels"

    s3_service = SplitDocument(
        local_path_pdfs, local_path_json, output_path
        )
    s3_service.prepare_dataset()
