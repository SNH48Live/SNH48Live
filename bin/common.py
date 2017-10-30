import logging
import pathlib
import sys
import traceback
import __main__

import appdirs


# Hierarchy:
#
# root
# ├── bin
# ├── config
# │   └── videos
# ├── data
# │   └── videos
# ├── thumbnails
# └── videos
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
BIN = ROOT / 'bin'
CONFIGS_DIR = ROOT / 'config'
VIDEO_CONFIGS_DIR = CONFIGS_DIR / 'videos'
DATA_DIR = ROOT / 'data'
VIDEO_METADATA_DIR = DATA_DIR / 'videos'
THUMBNAILS_DIR = ROOT / 'thumbnails'
VIDEOS_DIR = ROOT / 'videos'
CACHE_DIR = pathlib.Path(appdirs.user_cache_dir('SNH48Live', 'SNH48Live'))

_default_fmt = '[%(levelname)s] %(message)s'
_default_datefmt = '%Y-%m-%d %H:%M:%S'
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter(
    fmt=_default_fmt,
    datefmt=_default_datefmt,
))
logger = logging.getLogger('snh48live')
logger.addHandler(_handler)
logger.setLevel(logging.DEBUG)


def mail_on_exception():
    import config
    import mail

    def excepthook(etype, value, tb):
        try:
            script_name = pathlib.Path(__main__.__file__).name
        except AttributeError:
            script_name = 'script'

        if etype.__module__ == 'builtins':
            ename = etype.__name__
        else:
            ename = etype.__module__ + '.' + etype.__name__

        subject = f'[SNH48Live] {script_name} failed with {ename}'
        emsg = ''.join(traceback.format_exception(etype, value, tb))

        if config.main.notifications:
            mail.send_mail(subject, emsg, config.main.mailto)

        sys.stderr.write(emsg)
        sys.exit(1)

    if config.main.notifications:
        mail.init_gmail_client()
    sys.excepthook = excepthook


def change_logging_format(fmt=_default_fmt, datefmt=_default_datefmt):
    _handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
