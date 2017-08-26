import curses
import re
import shutil
import sys
import time

from common import logger


# A very bare-bones progress bar implementation. No speed or ETA support.
class ProgressBar(object):

    def __init__(self, total, *, update_threshold=1.0):
        self._total = total
        self._update_threshold = update_threshold
        #  536870912/4294967296 [===>   ]  80%
        self._fmt = '\r{{pos:{length}d}}/{total} [{{bar}}]{{percentage:4d}}%'.format(
            length=len(str(total)), total=total,
        )
        # Number of characters taken up by fixed-width components
        self._static_length = 2 * len(str(total)) + 9
        self._updated = 0
        self._pos = 0  # Last known position

        self._activated = False

    # Draw the bar and start responding to update() calls.
    def activate(self):
        # Hide cursor
        curses.setupterm()
        sys.stderr.buffer.write(curses.tigetstr('civis'))

        self.update(self._pos)
        self._activated = True

    def update(self, pos, *, force=False):
        self._pos = pos
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
        self._updated = time.time()

    # After calling done(), call activate() to redraw and re-activate the bar.
    def done(self):
        # Force update to last known pos, in case it wasn't printed due to the threshold
        self.update(self._pos, force=True)
        sys.stderr.write('\n')
        # Restore cursor
        sys.stderr.buffer.write(curses.tigetstr('cnorm'))
        self._activated = False


def sleep_until(datetime_):
    timestamp = datetime_.timestamp
    now = time.time()
    if now >= timestamp:
        return
    else:
        datetime_display = datetime_.to('local').strftime('%Y-%m-%d %H:%M %Z')
        logger.info(f'Sleeping until {datetime_display}...')
        time.sleep(timestamp - now)


# Convert a local, shortened title to a full title used formally.
def to_full_title(local_title):
    full_title = re.sub(r'^(\d{8}) ',
                        lambda m: f'{m.group(1)} SNH48 ',
                        local_title)
    full_title = full_title.replace('生日', '生日主题公演')
    return full_title
