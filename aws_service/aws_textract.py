from aws_service.aws_manager import AwsManager

from utils.prepare_aws_response import (
    get_textract_response
)
from utils.save_response import (
    save_response_json,
    save_text_plain
)


class AwsTextract(AwsManager):
    def __init__(self, bucket_name, folder_name, out_path_json, out_path_text):
        AwsManager.__init__(self, bucket_name, folder_name)
        self.out_path_json = out_path_json
        self.out_path_text = out_path_text

    def call_textract_service_dataset(self, filename):
        response = get_textract_response(self.bucket_name.name, filename)
        save_response_json(response, self.out_path_json, filename)
        save_text_plain(response, self.out_path_text, filename)
        return response

