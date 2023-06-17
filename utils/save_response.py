import json

from utils.utils import (
    makedirs,
)

JSON_EXTENSION = "json/"
TEXT_EXTENSION = "txts/"


def save_text_plain(response, output_path, filename):
    """Save information extracted from document as txt file"""
    if not response:
        return

    filename = _preprocess_filename_text(filename)
    filename = add_prefix(filename, TEXT_EXTENSION)
    makedirs(f"{output_path}/{TEXT_EXTENSION}")

    text_plain = _extract_plain_text(response)
    text_file = open(f"{output_path}/{filename}", mode="w", encoding="utf-8")
    text_file.write(text_plain)
    print(f"Text extracted from document {filename} and saved correctly!")
    text_file.close()


def save_response_json(response, output_path, filename):
    """Save information extracted from document as json file"""
    if not response:
        return

    filename = _preprocess_filename_json(filename)
    filename = add_prefix(filename, JSON_EXTENSION)
    makedirs(f"{output_path}/{JSON_EXTENSION}")

    with open(f"{output_path}/{filename}", mode="w", encoding="utf-8") as json_file:
        json.dump(response, json_file)


def add_prefix(filename: str, extension: str) -> str:
    """Add prefix to filename"""
    return extension + filename


def _extract_plain_text(response):
    text_plain = ""
    for slice_response in response:
        for block in slice_response["Blocks"]:
            if block["BlockType"] == "WORD":
                text_plain = text_plain + " " + block["Text"]
    text_plain = text_plain.strip()
    return text_plain


def _preprocess_filename_text(filename):
    filename = "/".join(filename.split("/")[1:])
    return f"{filename[:-4]}.txt"


def _preprocess_filename_json(filename):
    filename = "/".join(filename.split("/")[1:])
    return f"{filename[:-4]}.json"
