import json
import os
from os import listdir
from os.path import isfile, join
from typing import List, Dict


import numpy as np
import pandas as pd
from pdf2image import convert_from_path
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

from utils.get_words_and_coord_per_pages import (
    get_collection_of_words_coords_pages,
    get_collections_grouped_by_pages,
)


class SplitDocument():
    def __init__(self,
                 local_path_pdfs,
                 local_path_json,
                 output_path
                 ):
        self.local_path_pdfs = local_path_pdfs
        self.local_path_json = local_path_json
        self.output_path = output_path

    def prepare_dataset(self):
        filenames_pdf = [f for f in listdir(self.local_path_pdfs) if isfile(join(self.local_path_pdfs, f))]
        filenames_json = [self._convert_to_fname_suffix(f, 'json') for f in filenames_pdf]
        
        for f_json, f_pdf in zip(filenames_json, filenames_pdf):
            file = open(f"{self.local_path_json}/{f_json}")
            response = json.load(file) 

            #Get the list of words, coordinates and pages
            list_words, list_coordinates, list_pages = get_collection_of_words_coords_pages(response)

            # Get the list of words, coordinates and pages per pages
            grouped_words, grouped_coordinates = get_collections_grouped_by_pages(list_words,
                                                                                     list_coordinates,
                                                                                     list_pages)
            
            images = convert_from_path(f"{self.local_path_pdfs}/{f_pdf}",
                            dpi=300,
                            fmt="png")
            
            size_images = []
            for _, image in enumerate(images):
                np_image = _pilToNumpy(image)
                size_images.append(_get_width_height(np_image))

            paragraphs = self.split_doc_by_paragraphs(grouped_words, grouped_coordinates, size_images)
            sentences = self.split_doc_by_sentences(paragraphs)
            words = self.split_doc_by_words(sentences)
            _export_datasets_splited(words, self.output_path, f_pdf)



    def _convert_to_fname_suffix(self, filename: str, suffix: str) -> str:
        return f"{filename[:-3]}{suffix}"

    def split_doc_by_paragraphs(self, grouped_words, grouped_coordinates, size_images):

        words_grouped_by_position = []
        for idx, (words_per_pages, coord_per_pages) in enumerate(zip(grouped_words, grouped_coordinates)):
            idx_splits=[0]
            height, width = size_images[idx]
            for idx_token, (word, coordinate) in enumerate(zip(words_per_pages, coord_per_pages)):
                if idx_token == len(words_per_pages)-1:
                    idx_splits.append(len(words_per_pages))
                    words_grouped_by_position.append(words_per_pages[idx_splits[-2]:idx_splits[-1]])  
                    # width * coordinate["Left"] + 0.25*width < width * coord_per_pages[idx_token+1]["Left"] or 
                elif (coord_per_pages[idx_token+1]["Height"]<0.018 and height * coordinate["Top"] + 0.02*height < height * coord_per_pages[idx_token+1]["Top"]):
                    idx_splits.append(idx_token+1)
                    words_grouped_by_position.append(words_per_pages[idx_splits[-2]:idx_splits[-1]])
        
        return [' '.join(paragraph) for paragraph in words_grouped_by_position] 

    def split_doc_by_sentences(self, paragraphs: List[str]) -> List[Dict]:
        sentences = [sent_tokenize(text) for text in paragraphs]
        sentences = _flatten(sentences)
        sentences = [{'sentence_id': idx, 'text': sentence} for (idx, sentence) in enumerate(sentences)]
        return sentences
    
    def split_doc_by_words(self, sentences: List[Dict]) -> List[Dict]:
        words = [{'sentence_id': sentence['sentence_id'], 'words': word_tokenize(sentence['text'])} for sentence in sentences]
        return words


def _get_width_height(image):
    height, width, _ = image.shape
    return height, width


def _pilToNumpy(img):
    return np.array(img)


def _flatten(l):
    return [item for sublist in l for item in sublist]


def _export_datasets_splited(words: List[Dict], output_path: str, filename: str) -> None:
    df = pd.DataFrame(columns = ['sentence_id', 'words']) 
    for word in words:
        sentence_id = [word['sentence_id']]*len(word['words'])
        df=pd.concat([df, pd.DataFrame(list(zip(sentence_id, word['words'])),
               columns =['sentence_id', 'words'])], ignore_index=True)
    output_path = f"{output_path}/{filename}"
    exist_path = os.path.exists(output_path)
    if not exist_path:
        os.makedirs(output_path)
    df.to_csv(f"{output_path}/labels.csv", index = False)
