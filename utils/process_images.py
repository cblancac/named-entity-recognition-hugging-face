from typing import List, Tuple

import numpy as np
from PIL.PngImagePlugin import PngImageFile
from pdf2image import convert_from_path


class ProcessImage:
    """Class to process image files"""

    def __init__(self, filename: str):
        self.filename = filename

    def convert_pdf_to_images(self, file_path: str) -> List[PngImageFile]:
        """Take one pdf file and convert it to one image per page"""
        return convert_from_path(file_path, dpi=150, fmt="png")

    def get_size_per_image(self, images: List[PngImageFile]) -> List[Tuple[int]]:
        """Get the size of all the images in a document"""
        size_images = []
        for _, image in enumerate(images):
            np_image = self._pil_to_numpy(image)
            size_images.append(self._get_width_height(np_image))
        return size_images

    def process_filename(self) -> str:
        """Process the name of the file"""
        return "/".join(self.filename.split("/")[1:])

    def _get_width_height(self, image):
        height, width, _ = image.shape
        return height, width

    def _pil_to_numpy(self, img):
        return np.array(img)
