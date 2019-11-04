import curses
import curses.textpad


class TextField(curses.textpad.Textbox):
    """A derivation of the curses standard library Textbox.
    https://github.com/python/cpython/blob/master/Lib/curses/textpad.py

    TextField makes the following changes:
    1. `gather` moves the cursor back to its position before the call.
    2. `edit` takes a postprocessing callback after each keypress.
    """

    def gather(self):
        old_y, old_x = self.win.getyx()
        result = super().gather()
        self.win.move(old_y, old_x)
        return result

    def edit(self, validate=None, postprocess=None):
        while True:
            ch = self.win.getch()
            if validate:
                ch = validate(ch)
            if not ch:
                continue
            if not self.do_command(ch):
                break
            self.win.refresh()
            if postprocess:
                contents = (
                    self.gather().strip() if self.stripspaces else self.gather()
                )
                postprocess(contents, ch)
        return self.gather()
