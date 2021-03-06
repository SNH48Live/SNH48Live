import re
import sys

import arrow
import attrdict
import yaml

from common import CONFIGS_DIR, THUMBNAILS_DIR, VIDEO_CONFIGS_DIR, logger


CONFIG_FILE_PATTERN = re.compile(
    r'^(?P<date>\d{8})'
    r'-(bej|gnz|shy|ckg)?(?P<live_id>\d+)-'  # 0 for absence of live.snh48.com entry
    r'(?P<stage>.*?)'  # for one-off special performances, this is just
                       # the title or abbreviated title
    r'(-(?P<perfnum>\d{2}))?'  # only for performances within a regular stage
    r'\.yml$'
)


# Attributes
# - notifications: bool
# - mailto (optional): str
class MainConfig(object):
    def __init__(self):
        self.notifications = False
        self.mailto = None


# Load config/main.yml
def load_main_config():
    conf = MainConfig()

    config_file = CONFIGS_DIR / 'main.yml'
    if not config_file.exists():
        return conf
    with open(config_file) as fp:
        conf_dict = yaml.load(fp)
    if not conf_dict:
        return conf

    conf.notifications = conf_dict.get('notifications', False)
    conf.mailto = conf_dict.get('mailto')
    return conf


main = load_main_config()


# Attributes:
# - title: str
# - m3u8: str
# - starting_time: arrow.arrow.Arrow
# - vod: str
# - tags: List[str]
# - thumbnail (optional): str
# - playlists (playlist names): List[str]
class VodConfig(object):
    def __init__(self):
        self.title = None
        self.m3u8 = None
        self.starting_time = None
        self.vod = None
        self.tags = []
        self.thumbnail = None
        self.playlists = []
        self.public = None


def load_vod_config(config_file):
    with open(config_file) as fp:
        conf_dict = yaml.load(fp)

    conf = VodConfig()
    if 'title' in conf_dict:
        conf.title = conf_dict['title']
    else:
        logger.error(f'title not found in {config_file}')
        sys.exit(1)
    conf.m3u8 = conf_dict.get('m3u8')
    conf.vod = conf_dict.get('vod')
    # If datetime is not found in conf, use the current time.
    conf.starting_time = arrow.get(conf_dict.get('datetime'))
    conf.tags = conf_dict.get('tags', [])
    if 'SNH48' not in conf.tags:
        conf.tags.insert(0, 'SNH48')
    conf.thumbnail = conf_dict.get('thumbnail')
    if conf.thumbnail:
        conf.thumbnail = str(THUMBNAILS_DIR / 'generated' / conf.thumbnail)
    conf.playlists = conf_dict.get('playlists')

    return conf


# Returns a list of tuples (pathlib.Path, attrdict.AttrDict) where the former
# is the path to the config file, and the latter is an AttrDict with the
# following attributes, all str's: date, live_id, stage, and perfnum
# (optional).
def list_vod_configs(*, include_past=False, glob_pattern=None):
    if glob_pattern is None:
        glob_pattern = '**/*.yml' if include_past else '*.yml'

    conf_list = []
    for f in VIDEO_CONFIGS_DIR.glob(glob_pattern):
        m = CONFIG_FILE_PATTERN.match(f.name)
        if m:
            conf_list.append((f, attrdict.AttrDict(m.groupdict())))
        else:
            logger.warning(f"malformed filename '{f.name}'")
    conf_list.sort(key=lambda x: (x[1].date, int(x[1].live_id)))
    return conf_list


def reconstruct_filename(attrs):
    filename = f'{attrs.date}-{attrs.live_id}-{attrs.stage}'
    if attrs.perfnum is not None:
        filename += f'-{attrs.perfnum}'
    filename += '.yml'
    return filename
