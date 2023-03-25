import numpy as np
from pdf2image import convert_from_path


def convert_pdf_to_images(path_filename):
    return convert_from_path(path_filename, dpi=300, fmt="png")


def get_size_per_image(images):
    size_images = []
    
    for _, image in enumerate(images):
        np_image = _pilToNumpy(image)
        size_images.append(_get_width_height(np_image))
    return size_images


def _get_width_height(image):
    height, width, _ = image.shape
    return height, width


def _pilToNumpy(img):
    return np.array(img)


def process_filename(filename):
    return '/'.join(filename.split('/')[1:])