import numpy as np
from pdf2image import convert_from_path


class ProcessImage:
    def convert_pdf_to_images(self, path_filename):
        return convert_from_path(path_filename, dpi=300, fmt="png")

    def get_size_per_image(self, images):
        size_images = []
        for _, image in enumerate(images):
            np_image = self._pil_to_numpy(image)
            size_images.append(self._get_width_height(np_image))
        return size_images

    def process_filename(self, filename: str) -> str:
        return "/".join(filename.split("/")[1:])

    def _get_width_height(self, image):
        height, width, _ = image.shape
        return height, width

    def _pil_to_numpy(self, img):
        return np.array(img)
