import logging
import pathlib

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


def change_logging_format(fmt=_default_fmt, datefmt=_default_datefmt):
    _handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
