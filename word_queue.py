import collections
import random
from typing import List, Sequence


class WordQueue:
    NUM_ROWS: int = 3
    lexicon: Sequence[str]
    capacity: int
    row_queue: Sequence[List[str]]

    def __init__(self, lexicon, capacity):
        if isinstance(lexicon, str):
            with open(lexicon, "r") as f:
                self.lexicon = [line.strip() for line in f]
        else:
            self.lexicon = list(lexicon)
        self.capacity = capacity

        self.row_queue = collections.deque(
            [
                ["" for _ in range(self.capacity)],
                self._sample_row(),
                self._sample_row(),
            ],
            maxlen=self.NUM_ROWS,
        )

    def _sample_row(self) -> List[str]:
        return random.choices(self.lexicon, k=self.capacity)

    def prev_row(self) -> List[str]:
        return self.row_queue[0]

    def curr_row(self) -> List[str]:
        return self.row_queue[1]

    def next_row(self) -> List[str]:
        return self.row_queue[2]

    def advance(self):
        self.row_queue.append(self._sample_row())

    def __str__(self) -> str:
        prev_row = " ".join(self.prev_row())
        curr_row = " ".join(self.curr_row())
        next_row = " ".join(self.next_row())
        return f"{prev_row}\n{curr_row}\n{next_row}"
