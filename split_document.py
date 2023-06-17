from typing import List, Dict


import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

from utils.utils import (
    makedirs,
)
from utils.save_response import (
    add_prefix,
)

NER_EXTENSION = "ner_labels/"


class SplitDocument():
    """Class to split documents"""

    def split_doc_by_sentences(self, grouped_words, grouped_coordinates, size_images) -> List[Dict]:
        """Get paragraphs per documument and convert them into lists of sentences."""
        paragraphs = self._split_doc_by_paragraphs(grouped_words, grouped_coordinates, size_images)
        sentences = [sent_tokenize(text) for text in paragraphs]
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
        self, words: List[Dict], output_path: str, filename: str
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

        filename = add_prefix(filename, NER_EXTENSION)
        makedirs(f"{output_path}/{filename}")

        data_to_label.to_csv(f"{output_path}/{filename}/labels.csv", index=False)

    def _split_doc_by_paragraphs(self, grouped_words, grouped_coordinates, size_images):
        words_grouped_by_position = []
        for idx, (words_per_pages, coord_per_pages) in enumerate(
            zip(grouped_words, grouped_coordinates)
        ):
            idx_splits = [0]
            height, _ = size_images[idx]
            for idx_token, coordinate in enumerate(coord_per_pages):
                if idx_token == len(words_per_pages) - 1:
                    idx_splits.append(len(words_per_pages))
                    words_grouped_by_position.append(
                        words_per_pages[idx_splits[-2] : idx_splits[-1]]
                    )

                elif (
                    coord_per_pages[idx_token + 1]["Height"] < 0.018
                    and height * coordinate["Top"] + 0.02 * height
                    < height * coord_per_pages[idx_token + 1]["Top"]
                ):
                    idx_splits.append(idx_token + 1)
                    words_grouped_by_position.append(
                        words_per_pages[idx_splits[-2] : idx_splits[-1]]
                    )

        return [" ".join(paragraph) for paragraph in words_grouped_by_position]


def _flatten(sentences):
    return [item for sublist in sentences for item in sublist]
