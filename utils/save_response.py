import os
import json


def _extract_plain_text(response):
    text_plain = ""
    for i in range(len(response)):
        for block in response[i]['Blocks']:
            if block["BlockType"] == "WORD":
                text_plain = text_plain + " " + block["Text"]
    text_plain = text_plain.strip()
    return text_plain


def _preprocess_filename_text(filename):
    filename = '/'.join(filename.split("/")[1:])
    return f"{filename[:-4]}.txt"


def _preprocess_filename_json(filename):
    filename = '/'.join(filename.split("/")[1:])
    return f"{filename[:-4]}.json"


def save_text_plain(response, output_path, filename):
    
    if not response:
        return

    text_plain = _extract_plain_text(response)
    filename = _preprocess_filename_text(filename)

    exist_path = os.path.exists(output_path)
    if not exist_path:
        os.makedirs(output_path)

    text_file = open(f"{output_path}/{filename}", "w")
    text_file.write(text_plain)
    print(f"Text extracted from document {filename} and saved correctly!")
    text_file.close()


def save_response_json(response, output_path, filename):
    if not response:
        return
    
    filename = _preprocess_filename_json(filename)
    exist_path = os.path.exists(output_path)
    if not exist_path:
        os.makedirs(output_path)

    with open(f"{output_path}/{filename}", "w") as json_file:
        json.dump(response, json_file)