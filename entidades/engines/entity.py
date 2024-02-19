class Entity:
    def __init__(
            self, start: int = -1, end: int = -1, word: str = "", entity: str = "", score: float = 0.0, index: int = -1,
    ):
        self.start = start
        self.end = end
        self.word = word
        self.entity = entity
        self.score = score
        self.index = index

    def __repr__(self):
        return f"""Entity({str(self.start)}, {str(self.end)}, {self.word}, {self.entity})"""
    
    def _ensure_end_after_start(self):
        if self.end < self.start:
            raise ValueError("Entity cannot end before its start!")