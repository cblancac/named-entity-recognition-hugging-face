import numpy as np


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