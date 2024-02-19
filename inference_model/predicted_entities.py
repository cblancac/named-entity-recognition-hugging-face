from collections import defaultdict
from typing import Dict, DefaultDict, List


class PredictedEntities:
    """
    This class helps in building the dictionary of predictions. For each category
    we may have several predictions:
    category-A: "rat", "a mouse", "house"
    category-B: "3.2"

    Category names are not known in advance, and predictions may be given in
    fragments (e.g., "a mouse" is given as "a" and then "mouse").
    """

    def __init__(self, max_interval: int = 4):
        self._max_interval = max_interval

        self._last_find: Dict[str, int] = dict()
        self._preds: DefaultDict[str, List[str]] = defaultdict(list)

    def add_new(self, *, label: str, word: str, idx: int):
        self._last_find[label] = idx
        self._preds[label].append(word)

    def extend_last(self, *, label: str, word: str, idx: int):
        # default -10_000 ensures we can't extend an empty category
        last_seen = self._last_find.get(label, -10_000)
        if idx - last_seen <= self._max_interval:
            self._extend_last(label=label, word=word, idx=idx)
        else:
            self.add_new(label=label, word=word, idx=idx)

    def export_as_dict(self) -> Dict[str, List[str]]:
        return self._preds

    def _extend_last(self, *, label: str, word: str, idx: int):
        self._last_find[label] = idx
        self._preds[label][-1] += f" {word}"