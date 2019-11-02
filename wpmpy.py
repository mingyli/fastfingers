import argparse
import curses
import curses.ascii

from text_field import TextField
from word_queue import WordQueue
from performance import PerformanceMonitor

CTRL_A = 1
NEWLINE = 10
CTRL_K = 11
SPACE = 32
BACKSPACES = (curses.ascii.BS, curses.ascii.DEL, curses.KEY_BACKSPACE)


class Runner:
    performance_monitor = PerformanceMonitor()

    def __init__(self, lexicon):
        self.word_queue = WordQueue(lexicon)

    def report_performance(self):
        print(self.performance_monitor)

    def update_performance_window(self):
        self.performance_window.erase()
        self.performance_window.addstr(
            f"""
            Correct:   {self.performance_monitor.correct}
            Attempted: {self.performance_monitor.attempted}
            Accuracy:  {self.performance_monitor.accuracy}
            WPM:       {self.performance_monitor.wpm}
        """
        )
        self.performance_window.refresh()

    def update_display_window(self, prefix, suffix):
        self.display_window.erase()
        self.display_window.addstr(prefix)
        self.display_window.addstr(suffix, curses.A_BOLD)
        self.display_window.refresh()

    def validator(self, keystroke):
        return curses.ascii.BS if keystroke in BACKSPACES else keystroke

    def postprocessor(self, contents, keystroke):
        entered = contents
        expected = self.word_queue.front()

        prefix, suffix = self.word_queue.common_prefix(entered)
        self.update_display_window(prefix, suffix)
        self.update_performance_window()

        if keystroke in (SPACE, NEWLINE):
            self.performance_monitor.record(entered, expected)

            self.word_queue.proceed()
            self.update_display_window("", str(self.word_queue))

            # Move cursor to front and clear line.
            self.box.do_command(CTRL_A)
            self.box.do_command(CTRL_K)

    def init_windows(self, stdscr):
        rows, cols = stdscr.getmaxyx()
        self.title_window = stdscr.subwin(1, cols, 0, 0)
        self.display_window = stdscr.subwin(2, cols, 3, 0)
        self.entry_window = stdscr.subwin(1, cols, 6, 0)
        self.performance_window = stdscr.subwin(8, cols, 10, 0)

    def main(self, stdscr):
        self.init_windows(stdscr)

        self.display_window.addstr("wpmpy", curses.A_BOLD)
        self.display_window.addstr("\n")
        self.display_window.addstr("Hit a key to begin.")
        self.display_window.refresh()

        self.box = TextField(self.entry_window)

        _ = stdscr.getch()
        self.update_display_window("", str(self.word_queue))
        self.update_performance_window()
        self.title_window.addstr("Ctrl-G to exit.")
        self.title_window.refresh()

        with self.performance_monitor:
            _ = self.box.edit(
                validate=self.validator, postprocess=self.postprocessor
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--lexicon",
        type=str,
        help="Path to a list of words.",
        default="top1000.txt",
    )
    args = parser.parse_args()

    runner = Runner(args.lexicon)
    curses.wrapper(runner.main)
    runner.report_performance()
