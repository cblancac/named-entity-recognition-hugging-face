from pathlib import Path
from typing import Dict, List

from nltk.tokenize import sent_tokenize
import numpy as np
from tqdm.auto import tqdm
from torch.utils.data import DataLoader, SequentialSampler
import torch
from transformers import (
    RobertaConfig,
    RobertaForTokenClassification,
    RobertaTokenizerFast,
)
from model import XLMRobertaForTokenClassification

from inference_model.predicted_entities import PredictedEntities
from inference_model.token_prediction import TokenPrediction


MODEL_TYPE = "roberta"

class NerInferencer:
    def __init__(
            self, sentences, model_ckpt,
        ):
        self.sentences = sentences
        self.model_ckpt = model_ckpt
        self.pad_token_label_id = -100
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.config_class, _, self.tokenizer_class = self._get_config_and_tokenizer_classes(MODEL_TYPE)

    def inference(self):
        tokenizer = self._get_tokenizer()
        model = self._get_model()
        model_inputs = self._encode(tokenizer, self.sentences)
        encoded_model_inputs = self._change_shape_for_batching(model_inputs)
        preds, out_label_ids = self._get_preds_and_label_ids(self.sentences, encoded_model_inputs, tokenizer, model)
        bio_entities_predicted = self._get_bio_predictions(self.sentences, preds, out_label_ids, model)
        entities = self._process_ner_predictions(bio_entities_predicted)
        return entities


    def _get_config_and_tokenizer_classes(self, model_type: str):
        model_classes = {"roberta": (RobertaConfig(torchscript=True), RobertaForTokenClassification, RobertaTokenizerFast)}
        return model_classes[model_type]
    
    def _get_tokenizer(self):
        return self.tokenizer_class.from_pretrained(
            Path(self.model_ckpt), do_lower_case=True)
        
    def _get_model(self):
        return XLMRobertaForTokenClassification.from_pretrained(self.model_ckpt).to(self.device)

    def _encode(self, tokenizer, to_predict: List[str]):
        return tokenizer.batch_encode_plus(
            to_predict,
            return_tensors="pt",
            padding=True,
            truncation=True,
            is_split_into_words=False
        )
    
    def _change_shape_for_batching(self, model_inputs):
        encoded_model_inputs = []
        for (input_ids, attention_mask) in tqdm(zip(model_inputs["input_ids"], model_inputs["attention_mask"])):
            encoded_model_inputs.append((input_ids, attention_mask))
        return encoded_model_inputs
    
    def _get_preds_and_label_ids(self, to_predict, encoded_model_inputs, tokenizer, model):
        preds = None

        # Setup batches
        eval_sampler = SequentialSampler(encoded_model_inputs)
        eval_dataloader = DataLoader(
            encoded_model_inputs,
            sampler=eval_sampler,
            batch_size=1,
        )
        for batch in tqdm(
            eval_dataloader, disable=True, desc="Running Prediction"
        ):
        
            batch = tuple(t.to(self.device) for t in batch)
            inputs = {
                "input_ids": batch[0],
                "attention_mask": batch[1],
            }


            output = model(inputs["input_ids"], inputs["attention_mask"])

            if preds is None:
                preds = output[0].detach().cpu().numpy()
                out_input_ids = inputs["input_ids"].detach().cpu().numpy()
                out_attention_mask = inputs["attention_mask"].detach().cpu().numpy()
            else:
                preds = np.append(preds, output[0].detach().cpu().numpy(), axis=0)
                out_input_ids = np.append(
                    out_input_ids, inputs["input_ids"].detach().cpu().numpy(), axis=0
                )
                out_attention_mask = np.append(
                    out_attention_mask, inputs["attention_mask"].detach().cpu().numpy(), axis=0
                )

        out_label_ids = [[] for _ in range(len(to_predict))]
        max_len = len(out_input_ids[0])

        for index, sentence in enumerate(to_predict):
            for word in sentence.split():
                word_tokens = tokenizer.tokenize(word)
                out_label_ids[index].extend(
                    [0] + [self.pad_token_label_id] * (len(word_tokens) - 1)
                )

            out_label_ids[index].insert(0, self.pad_token_label_id)
            out_label_ids[index].append(self.pad_token_label_id)

            if len(out_label_ids[index]) < max_len:
                out_label_ids[index].extend(
                    [-100] * (max_len - len(out_label_ids[index]))
                )
            
            # When the tokenization of the sentence is too long, truncate it
            # TODO: Split the sentence previously if it is longer than 1_000
            # characters, saving the information before calling thus method
            if len(out_label_ids[index]) > max_len:
                out_label_ids[index] = out_label_ids[index][:max_len]

        out_label_ids = np.array(out_label_ids).reshape(len(out_label_ids), max_len)
        return preds, out_label_ids
    
    def _get_bio_predictions(self, to_predict, preds, out_label_ids, model):
        #preds = preds.cpu().detach().numpy()
        preds = np.argmax(preds, axis=2)

        out_label_list = [[] for _ in range(out_label_ids.shape[0])]
        preds_list = [[] for _ in range(out_label_ids.shape[0])]

        label_map = model.config.id2label

        for i in range(out_label_ids.shape[0]):
            for j in range(out_label_ids.shape[1]):
                if out_label_ids[i, j] != self.pad_token_label_id:
                    out_label_list[i].append(label_map[out_label_ids[i][j]])
                    preds_list[i].append(label_map[preds[i][j]])

        preds = [
            [
                {word: preds_list[i][j]}
                for j, word in enumerate(sentence.split()[: len(preds_list[i])])
            ]
            for i, sentence in enumerate(to_predict)
        ]
        return preds
    
    def _process_ner_predictions(
        self, predictions: List[List[Dict[str, str]]], margin: int = 4
    ) -> Dict[str, List[str]]:

        predictions = _flatten_list(predictions)
        preds = [TokenPrediction(x) for x in predictions]
        entities = PredictedEntities(max_interval=margin)

        for token_idx, token_pred in enumerate(preds):
            if token_pred.is_empty():
                continue

            label = token_pred.get_label()
            word = token_pred.get_word()
            if token_pred.is_start():
                entities.add_new(label=label, word=word, idx=token_idx)
            else:
                entities.extend_last(label=label, word=word, idx=token_idx)
        return entities.export_as_dict()


def _flatten_list(list: List[list]) -> list:
    return [x for sub_list in list for x in sub_list]