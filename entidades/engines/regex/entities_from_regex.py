from typing import List

import regex as re

from entidades.engines.entity import Entity


def entities_from_regex(
    pattern: re.Pattern,
    text: str,
    category: str,
) -> List[Entity]:
    matches = pattern.finditer(text)
    entities = [
        Entity(
            start=match.start(),
            end=match.end(),
            word=match.group(0),
            entity=category,
            score=1,
            index=-1
        )
        for match in matches
    ]
    return entities
