from typing import List, Dict

from entidades.engines.ner import Ner


def _flatten_sum(matrix):
    return sum(matrix, [])


def merge_entities(dict_1, dict_2):
   dict_3 = {**dict_1, **dict_2}
   for key, value in dict_3.items():
       if key in dict_1 and key in dict_2:
               dict_3[key] = _flatten_sum([value , dict_1[key]])
   return dict_3


def entities_from_one_doc(sentences: List[str], ner_regex: Ner, ner_neural: Ner) -> List[Dict]:
    """Inference: Given a plain text, extract the entities"""
    entities_regex = ner_regex.extract_entities_from_text(sentences)
    entities_neural = ner_neural.extract_entities_from_text(sentences)
    return merge_entities(entities_neural, entities_regex)
