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


def common_prefix(s1, s2):
    index = 0
    while index < min(len(s1), len(s2)):
        if s1[index] != s2[index]:
            break
        index += 1
    return s1[:index], s1[index:]


class Runner:
    performance_monitor = PerformanceMonitor()

    def __init__(self, lexicon, num_words):
        self.capacity = num_words
        self.word_queue = WordQueue(lexicon, num_words)
        self.history = []

    def performance_report(self):
        return str(self.performance_monitor)

    def render_performance_window(self):
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

    def render_display_window(self, contents=""):
        self.display_window.erase()

        for i in range(len(self.word_queue.curr_row())):
            word = self.word_queue.curr_row()[i]

            if i < self.curr_position():
                entry = self.history[i]
                prefix_color = (
                    self.red_color
                    if entry != word and entry.startswith(word)
                    else curses.A_BOLD
                )
                suffix_color = self.red_color
            elif i == self.curr_position():
                entry = contents
                prefix_color = curses.A_BOLD
                suffix_color = curses.A_REVERSE
            else:
                entry = word
                prefix_color = curses.A_NORMAL
                suffix_color = curses.A_NORMAL

            prefix, suffix = common_prefix(word, entry)
            self.display_window.addstr(prefix, prefix_color)
            self.display_window.addstr(suffix, suffix_color)
            self.display_window.addstr(" ")
        self.display_window.addstr("\n")
        self.display_window.addstr(" ".join(self.word_queue.next_row()))

        self.display_window.refresh()

    def curr_position(self):
        return len(self.history)

    def validator(self, keystroke):
        if keystroke in (SPACE, NEWLINE):
            return SPACE
        elif keystroke in BACKSPACES:
            return curses.ascii.BS
        else:
            return keystroke

    def postprocessor(self, contents, keystroke):
        if keystroke in (SPACE, NEWLINE):
            expected = self.word_queue.curr_row()[self.curr_position()]
            self.performance_monitor.record(contents, expected)
            self.history.append(contents)

            if len(self.history) == self.capacity:
                self.word_queue.advance()
                self.history = []

            self.render_display_window()
            self.render_performance_window()

            # Move cursor to front and clear line.
            self.box.do_command(CTRL_A)
            self.box.do_command(CTRL_K)
        else:
            self.render_display_window(contents=contents)
            self.render_performance_window()

    def init_windows(self, stdscr, margin=4):
        rows, cols = stdscr.getmaxyx()
        self.title_window = stdscr.subwin(1, cols, 0, 0)
        self.display_window = stdscr.subwin(2, cols - margin, 3, margin)
        self.entry_window = stdscr.subwin(1, cols - margin, 6, margin)
        self.performance_window = stdscr.subwin(8, cols, 10, 0)

    def init_colors(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        self.red_color = curses.color_pair(1)

    def main(self, stdscr):
        self.init_windows(stdscr)
        self.init_colors()

        self.display_window.addstr("fastfingers", curses.A_BOLD)
        self.display_window.addstr("\n")
        self.display_window.addstr("Hit a key to begin.")
        self.display_window.refresh()

        self.box = TextField(self.entry_window)

        _ = stdscr.getch()
        self.render_display_window()
        self.render_performance_window()
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
    parser.add_argument(
        "--num_words",
        type=int,
        help="The number of words to display in each row.",
        default=9,
    )
    args = parser.parse_args()

    runner = Runner(args.lexicon, args.num_words)
    curses.wrapper(runner.main)
    print(runner.performance_report())
