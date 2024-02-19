from typing import Dict


class TokenPrediction:
    """
    This class helps in handling predictions of the form:
    some_word: label

    Where labels are:
    O for None
    B-label for start of label
    I-label for continuation of label
    """

    def __init__(self, token_prediction: Dict[str, str]):
        self._raw_pred = token_prediction

    def get_label(self):
        label = self._get_whole_label()
        return label[2:]

    def get_word(self) -> str:
        return list(self._raw_pred.keys())[0]

    def is_empty(self) -> bool:
        return self._get_whole_label() == "O"

    def is_start(self) -> bool:
        return self._get_whole_label().startswith("B")

    def _get_whole_label(self):
        return list(self._raw_pred.values())[0]