from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from split_document import SplitDocument

if __name__ == "__main__":

    local_path_pdfs = "data/preprocess/pdfs"
    local_path_json = "data/preprocess/json"
    output_path = "data/preprocess/ner_labels"

    s3_service = SplitDocument(
        local_path_pdfs, local_path_json, output_path
        )
    s3_service.prepare_dataset()
