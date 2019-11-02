import collections
import random


class WordQueue:
    def __init__(self, lexicon, capacity=10):
        self.lexicon = lexicon
        self.queue = collections.deque(
            random.choices(lexicon, k=capacity), maxlen=capacity
        )

    def _sample(self):
        return random.choice(self.lexicon)

    def proceed(self):
        self.queue.append(self._sample())

    def __str__(self):
        return " ".join(self.queue)

    def front(self):
        return self.queue[0]

    def common_prefix(self, s2):
        index = 0
        s1 = str(self)
        while index < min(len(s1), len(s2)):
            if s1[index] != s2[index]:
                break
            index += 1
        return s1[:index], s1[index:]
