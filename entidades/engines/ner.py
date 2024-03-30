from abc import ABC, abstractmethod
from pathlib import Path
import sys
from typing import List, Dict

import torch
from transformers import AutoTokenizer
#from transformers import pipeline

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from entidades.engines.neural.entities_from_neural import entities_from_neural
from entidades.engines.regex.regex_pattern import apply_all
from inference_model.ner_inferencer import NerInferencer
from model import XLMRobertaForTokenClassification

# Specify the path of the model
model_ckpt = Path("./models/xlm-roberta-base-investing-ner")

# Load the fine-tuned tokenizer and model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
model = XLMRobertaForTokenClassification.from_pretrained(model_ckpt).to(device)


class Ner(ABC):
    """Create a NER class"""

    @abstractmethod
    def extract_entities_from_text(self, text: str) -> List[Dict]:
        raise NotImplementedError


class NerNeural(Ner):
    """Child from Ner class: extract entities using neural network"""

    def extract_entities_from_text(self, text: str) -> List[Dict]:
        # method 1:
        #TODO: In case we need to work with positions. 
        #model = XLMRobertaForTokenClassification.from_pretrained(model_ckpt)
        #nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
        #entities = nlp(text)
        # method 2:
        pipeline = NerInferencer(text, model_ckpt)
        entities = pipeline.inference()
        return entities_from_neural(entities)


class NerRegex(Ner):
    """Child from Ner class: extract entities using regular expression"""

    def extract_entities_from_text(self, text: str) -> List[Dict]:
        return apply_all(text)
        