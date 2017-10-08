import json
import re

from common import DATA_DIR, logger


PLAYLISTS_JSON = DATA_DIR / 'playlists.json'
with open(PLAYLISTS_JSON) as fp:
    PLAYLISTS_MAP = json.load(fp)

PLAYLIST_ID_PATTERN = re.compile('^[a-zA-Z0-9_-]{34}$')


def name2id(playlist_name, report_error=True):
    playlist_id = PLAYLISTS_MAP.get(playlist_name)
    if not playlist_id and report_error:
        logger.error(f'playlist named {playlist_name} not found in {PLAYLISTS_JSON}')
    return playlist_id


def list_videos(youtube, playlist_id, part='contentDetails'):
    request = youtube.playlistItems().list(
        playlistId=playlist_id,
        part=part,
        maxResults=50,
    )
    videos = []
    while request:
        response = request.execute()
        videos.extend(response['items'])
        request = youtube.playlistItems().list_next(request, response)
    return videos
