import sys

import arrow
import yaml

from common import THUMBNAILS_DIR, logger


class Config(object):
    def __init__(self):
        # Set potential properties the stupid way (not using setattr) to
        # silence pylint errors/warnings.
        self.title = None
        self.m3u8 = None
        self.starting_time = None
        self.vod = None
        self.tags = []
        self.thumbnail = None
        self.playlists = []
        self.public = None


# Attributes:
# - title: str
# - m3u8: str
# - starting_time: arrow.arrow.Arrow
# - vod: str
# - tags: List[str]
# - thumbnail (optional): str
# - playlists (playlist names): List[str]
def load_config(config_file):
    with open(config_file) as fp:
        conf_dict = yaml.load(fp)

    conf = Config()
    for attr in ('title', 'm3u8'):
        if attr in conf_dict:
            setattr(conf, attr, conf_dict[attr])
        else:
            logger.error(f'{attr} not found in {config_file}')
            sys.exit(1)
    # If datetime is not found in conf, use the current time.
    conf.starting_time = arrow.get(conf_dict.get('datetime'))
    conf.vod = conf_dict.get('vod', 'http://live.snh48.com/')
    conf.tags = conf_dict.get('tags', [])
    if 'SNH48' not in conf.tags:
        conf.tags.insert(0, 'SNH48')
    conf.thumbnail = conf_dict.get('thumbnail')
    if conf.thumbnail:
        conf.thumbnail = str(THUMBNAILS_DIR / 'generated' / conf.thumbnail)
    conf.playlists = conf_dict.get('playlists')

    return conf
