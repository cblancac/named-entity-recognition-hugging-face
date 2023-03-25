import os
from typing import List, Dict


import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize


class SplitDocument():
    def __init__(self,output_path):
        self.output_path = output_path

    def split_doc_by_paragraphs(self, grouped_words, grouped_coordinates, size_images):

        words_grouped_by_position = []
        for idx, (words_per_pages, coord_per_pages) in enumerate(zip(grouped_words, grouped_coordinates)):
            idx_splits=[0]
            height, _ = size_images[idx]
            for idx_token, coordinate in enumerate(coord_per_pages):
                if idx_token == len(words_per_pages)-1:
                    idx_splits.append(len(words_per_pages))
                    words_grouped_by_position.append(words_per_pages[idx_splits[-2]:idx_splits[-1]])  

                elif (coord_per_pages[idx_token+1]["Height"]<0.018 and 
                      height * coordinate["Top"] + 0.02*height < height * coord_per_pages[idx_token+1]["Top"]):
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
    
    def _export_datasets_splited(self, words: List[Dict], output_path: str, filename: str) -> None:
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


def _flatten(l):
    return [item for sublist in l for item in sublist]
