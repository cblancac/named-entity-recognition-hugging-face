import os
from pathlib import Path
from os import listdir
from os.path import isfile, join

import ast
from datasets import load_dataset
import pandas as pd


class Dataset():
    def __init__(self, datasets_path: Path, dataset_filename: str):
        self.datasets_path    = datasets_path
        self.dataset_filename = dataset_filename
        self.export_path      = datasets_path / dataset_filename
        self.complete_dataset = pd.DataFrame()
        self.raw_dataset      = pd.DataFrame()

    def create_dataset_csv(self):
        self._delete_old_files_in_folder()

        dataset_folders = [f for f in listdir(self.datasets_path)]
        for dataset_folder in dataset_folders:
            dataset = pd.read_csv(self.datasets_path / dataset_folder / "labels.csv", encoding = "ISO-8859-1")
            dataset["labels"] = dataset["labels"].fillna('O')
            dataset = dataset[dataset["words"].notna()]
            dataset["filename"] = dataset_folder
            self._update_row_dataset(dataset)
            dataset = self._format_hf_dataset(dataset)
            self._update_complete_dataset(dataset)

        self._export_dataset(
            self.complete_dataset,
            self.dataset_filename
        )

    def split_train_test(self, train_size: float = 0.8):
        filenames = self.complete_dataset["filename"].unique()
        n_files = len(filenames)
        filenames_train = filenames[:int(n_files*train_size)]
        filenames_test  = filenames[int(n_files*train_size):]

        train_dataset = self.complete_dataset[self.complete_dataset["filename"].isin(filenames_train)]
        test_dataset  = self.complete_dataset[self.complete_dataset["filename"].isin(filenames_test)]

        self._export_dataset(train_dataset, "train_dataset.csv")
        self._export_dataset(test_dataset, "test_dataset.csv")

    def load_hf_dataset(self):
        dataset = load_dataset("csv", data_files={
            "train": str(self.datasets_path)+"/train_dataset.csv", 
            "test": str(self.datasets_path)+"/test_dataset.csv"}
        )
        dict_int2str, self.dict_str2int, num_classes = self._create_dict_labels()
        dataset = dataset.map(self._reconstract_objects)
        return dataset.map(self._create_tag_int), dict_int2str, self.dict_str2int, num_classes
        
    def _create_tag_int(self, batch):
        return {"ner_tags": [self.dict_str2int[n] for n in batch["ner_tags_str"]]}

    def _reconstract_objects(self, batch):
        return {"tokens": ast.literal_eval(batch["tokens"]), "ner_tags_str": ast.literal_eval(batch["ner_tags_str"])}

    def _create_dict_labels(self):
        #select unique labels
        labels = self.raw_dataset["labels"].unique()
        num_classes = len(labels)
        dict_int2str = dict(list(enumerate(labels)))
        dict_str2int = {value:key for key, value in dict_int2str.items()}
        return dict_int2str, dict_str2int, num_classes

    def _delete_old_files_in_folder(self):
        files_to_delete = [f for f in listdir(self.datasets_path) if isfile(join(self.datasets_path, f))]
        for file in files_to_delete:
            os.remove(self.datasets_path / file)
        
    def _update_complete_dataset(self, dataset: pd.DataFrame):
        self.complete_dataset = pd.concat([self.complete_dataset, dataset], axis=0)

    def _update_row_dataset(self, dataset: pd.DataFrame):
        self.raw_dataset = pd.concat([self.raw_dataset, dataset], axis=0)
        
    def _export_dataset(self, df, filename: str):
        df.to_csv(self.datasets_path / filename, index=False)

    def _format_hf_dataset(self, dataset: pd.DataFrame):
        dataset.rename(columns = {
                                    'words':'tokens', 
                                    'labels':'ner_tags_str', 
                                    'sentence_id': 'idx_sentence'
                                    }, inplace = True)
        
        return dataset.groupby(
                        ['idx_sentence', 'filename'], as_index = False
                        ).agg({'tokens': list, 'ner_tags_str': list}
                    )