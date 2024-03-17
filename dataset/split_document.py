import os
from typing import List, Dict
from PIL.PngImagePlugin import PngImageFile
from langchain_text_splitters import TokenTextSplitter

import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

TEMP_FOLDER = "temp"


class SplitDocument:
    """Class to split documents"""

    def __init__(
        self,
        grouped_words: List[List[str]],
        grouped_coordinates: List[List[str]],
        size_images: List[PngImageFile],
    ):
        self.grouped_words = grouped_words
        self.grouped_coordinates = grouped_coordinates
        self.size_images = size_images
        self.text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=0)


    def split_doc_by_sentences(self) -> List[Dict]:
        """Get paragraphs per documument and convert them into lists of sentences."""
        paragraphs = self._split_doc_by_paragraphs()
        sentences = [sent_tokenize(text) if len(text)>800 else [text] for text in paragraphs]
        sentences = _flatten(sentences)
        sentences = [self.text_splitter.split_text(sentence) for sentence in sentences]
        sentences = _flatten(sentences)
        sentences = [
            {"sentence_id": idx, "text": sentence}
            for (idx, sentence) in enumerate(sentences)
        ]
        return sentences

    def split_doc_by_words(self, sentences: List[Dict]) -> List[Dict]:
        """Get list of words per sentences."""
        words = [
            {
                "sentence_id": sentence["sentence_id"],
                "words": word_tokenize(sentence["text"]),
            }
            for sentence in sentences
        ]
        return words

    def export_datasets_splited(
        self, words: List[Dict], output_path: str,
    ) -> None:
        """Export to csv the information related to sentence and their words."""
        data_to_label = pd.DataFrame(columns=["sentence_id", "words"])
        for word in words:
            sentence_id = [word["sentence_id"]] * len(word["words"])
            data_to_label = pd.concat(
                [
                    data_to_label,
                    pd.DataFrame(
                        list(zip(sentence_id, word["words"])),
                        columns=["sentence_id", "words"],
                    ),
                ],
                ignore_index=True,
            )

        data_to_label.to_csv(f"{TEMP_FOLDER}/{output_path}", index=False)

    def clean_temporary_files(self, path: str) -> None:
        """Delete csv file when it is uploaded to s3"""
        os.remove(f"{TEMP_FOLDER}/{path}")

    def _split_doc_by_paragraphs(self):
        words_grouped_by_position = []
        for idx, (words_per_pages, coord_per_pages) in enumerate(
            zip(self.grouped_words, self.grouped_coordinates)
        ):
            idx_splits = [0]
            height, _ = self.size_images[idx]
            for idx_token, coordinate in enumerate(coord_per_pages):
                if idx_token == len(words_per_pages) - 1:
                    idx_splits.append(len(words_per_pages))
                    words_grouped_by_position.append(
                        words_per_pages[idx_splits[-2] : idx_splits[-1]]
                    )

                elif height * coordinate["Top"] + 0.03 * height < height * coord_per_pages[idx_token + 1]["Top"]:
                    idx_splits.append(idx_token + 1)
                    words_grouped_by_position.append(
                        words_per_pages[idx_splits[-2] : idx_splits[-1]]
                    )

        return [" ".join(paragraph) for paragraph in words_grouped_by_position]


def _flatten(sentences):
    return [item for sublist in sentences for item in sublist]
