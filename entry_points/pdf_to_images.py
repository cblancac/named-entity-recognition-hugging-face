import os
from pdf2image import convert_from_path


if __name__ == '__main__':
    
    directory = "data/preprocess/pdfs"
    output_folder = "data/preprocess/imgs"
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        image = convert_from_path(path,
                                dpi=300,
                                fmt="png")
        for page in range(len(image)):
            image[page].save(f"{output_folder}/{filename.split('.pdf')[0]}_{page}.png")