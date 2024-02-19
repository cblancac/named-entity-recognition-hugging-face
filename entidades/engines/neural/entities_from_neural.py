from typing import List, Dict

from entidades.engines.entity import Entity


def entities_from_neural(entities: List[Dict]) -> List[Entity]:
    return [
        Entity(e["start"], e["end"], e["word"], e["entity_group"], e["score"])
        for e in entities
    ]
