from abc import ABC, abstractmethod
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from entidades.user_cases.entities_from_one_doc import entities_from_one_doc
from entidades.engines.ner import (
    NerRegex,
    NerNeural,
)
from entidades.input_output.file_manager import (
    FileManager,
    TxtFromPdfMiner,
    TxtFromTextract,
    TxtFromPytesseract,
)


class TextFromDoc(ABC):
    """Create the father class to choose the
    reader of documents"""

    @abstractmethod
    def get_reader(self, type: str):
        """Return the FileManager choosen"""
        raise NotImplementedError

class TextFromDocImpl(TextFromDoc):
    """Implementation of TextFromDoc, choose one
    option to read document"""

    def get_reader(self, type: str) -> FileManager:
        dict = {
                    "pdf": TxtFromPdfMiner(),
                    "aws": TxtFromTextract(),
                    "img": TxtFromPytesseract(),
                }
        return dict[type]


def main(filename: str) -> None:
    """Given a document, choose the reader to use
    and extract the entities from it"""
    type_reader = str(
        input(
            """
    [pdf]Para utilizar PDF Miner
    [aws]Para utilizar Textract
    [img]Para utilizar Pytesseract
    >>>: """
        )
    )

    reader_doc = TextFromDocImpl().get_reader(type=type_reader)
    text = reader_doc.load_info_from_doc(filename)
    ner_regex = NerRegex()
    ner_neural = NerNeural()

    entities = entities_from_one_doc(text, ner_regex, ner_neural)
    print(entities)


if __name__ == "__main__":
    FILENAME = "6 big dividends_ Jackson Financial hikes, Saratoga keeps jumbo yield _ Pro Recap By Investing.com.pdf"
    main(FILENAME)
