import time


class PerformanceMonitor:
    begin_time: float = 0.0
    end_time: float = 0.0
    correct: int = 0
    attempted: int = 0

    def begin(self):
        self.begin_time = time.time()

    def end(self):
        self.end_time = time.time()

    def record(self, entered: str, expected: str):
        if entered == expected:
            self.correct += 1
        self.attempted += 1

    @property
    def duration(self) -> float:
        if self.end_time:
            return self.end_time - self.begin_time
        else:
            return time.time() - self.begin_time

    @property
    def accuracy(self) -> float:
        if self.attempted == 0:
            return 0.0
        else:
            return self.correct / self.attempted

    @property
    def wpm(self) -> float:
        if self.duration == 0.0:
            return 0.0
        else:
            return self.correct / self.duration * 60.0

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end()

    def __str__(self) -> str:
        return f"""
            Correct:   {self.correct}
            Attempted: {self.attempted}
            Accuracy:  {self.accuracy}
            Duration:  {self.duration}
            WPM:       {self.wpm}
        """
