import curses
import os
import shutil
import sys
import time


# A very bare-bones progress bar implementation. No speed or ETA support.
class ProgressBar(object):

    def __init__(self, total, *, update_threshold=0.1):
        self._total = total
        self._update_threshold = update_threshold
        #  536870912/4294967296 [===>   ]  80%
        self._fmt = '\r{{pos:{length}d}}/{total} [{{bar}}]{{percentage:4d}}%'.format(
            length=len(str(total)), total=total,
        )
        # Number of characters taken up by fixed-width components
        self._static_length = 2 * len(str(total)) + 9
        self._updated = 0

        self._activated = False

    # Draw the bar and start responding to update() calls.
    def activate(self):
        # Hide cursor
        curses.setupterm()
        sys.stderr.buffer.write(curses.tigetstr('civis'))

        self.update(0)
        self._activated = True

    def update(self, pos, *, force=False):
        if not self._activated:
            return
        if not force and time.time() - self._updated < self._update_threshold:
            return
        percentage = int(pos / self._total * 100)
        term_width, _ = shutil.get_terminal_size()
        bar_length = max(40, term_width - 1 - self._static_length)
        filled_length = max(int(bar_length * pos / self._total), 1)
        bar = '=' * (filled_length - 1) + '>' + ' ' * (bar_length - filled_length)
        sys.stderr.write(self._fmt.format(
            pos=pos, bar=bar, percentage=percentage,
        ))

    # After calling done(), call activate() to redraw and re-activate the bar.
    def done(self):
        sys.stderr.write('\n')
        # Restore cursor
        sys.stderr.buffer.write(curses.tigetstr('cnorm'))
        self._activated = False
