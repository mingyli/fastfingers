import collections
import random


class WordQueue:
    NUM_ROWS = 3

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

    def _sample_row(self):
        return random.choices(self.lexicon, k=self.capacity)

    def prev_row(self):
        return self.row_queue[0]

    def curr_row(self):
        return self.row_queue[1]

    def next_row(self):
        return self.row_queue[2]

    def advance(self):
        self.row_queue.append(self._sample_row())

    def __str__(self):
        prev_row = " ".join(self.prev_row())
        curr_row = " ".join(self.curr_row())
        next_row = " ".join(self.next_row())
        return f"{prev_row}\n{curr_row}\n{next_row}"
