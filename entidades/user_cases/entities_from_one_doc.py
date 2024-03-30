from typing import List, Dict

from entidades.engines.ner import Ner

def entities_from_one_doc(sentences: List[str], ner_regex: Ner, ner_neural: Ner) -> List[Dict]:
    """Inference: Given a plain text, extract the entities"""
    text = " ".join(sentences)
    entities_regex = ner_regex.extract_entities_from_text(text)
    entities_neural = ner_neural.extract_entities_from_text(sentences)
    return entities_regex, entities_neural
