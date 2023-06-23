from abc import ABC, abstractmethod
from typing import List, Dict

class PreprocessFile(ABC):
    """Class to preprocess files"""

    @abstractmethod
    def get_collections_grouped_by_pages(self) -> None:
        """Get words and coordinates grouped by page"""


class PreprocessPDF(PreprocessFile):
    """Class to preprocess PDF"""

    def __init__(self, response: List[Dict]):
        self.response = response

    def get_collections_grouped_by_pages(self):
        (
            list_words,
            list_coordinates,
            list_pages,
        ) = self._get_collection_of_words_coords_pages(self.response)

        # Get the list with the whole information of the bounding boxes: (words, coordinates, pages)
        zip_list = list(zip(list_words, list_coordinates, list_pages))

        # Get the uniques pages
        unique_pages = list({z[2] for z in zip_list})

        # Group the words and coordinates by pages
        grouped_words = [
            [list[0] for list in zip_list if list[2] == value] for value in unique_pages
        ]
        grouped_coordinates = [
            [list[1] for list in zip_list if list[2] == value] for value in unique_pages
        ]
        return grouped_words, grouped_coordinates

    def _get_collection_of_words_coords_pages(self, response):
        list_words, list_coordinates, list_pages = [], [], []
        for slice_response in response:
            for block in slice_response["Blocks"]:
                if block["BlockType"] == "WORD":
                    for word in block["Text"].split():
                        list_words.append(word)
                        list_coordinates.append(block["Geometry"]["BoundingBox"])
                        list_pages.append(block["Page"])
        return list_words, list_coordinates, list_pages
