import argparse

import googleapiclient.discovery
import httplib2
import oauth2client.client
import oauth2client.file
import oauth2client.tools

from common import CONFIGS_DIR


YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_ANALYTICS_API_SERVICE_NAME = 'youtubeAnalytics'
YOUTUBE_ANALYTICS_API_VERSION = 'v1'

CLIENT_SECRETS_FILE = CONFIGS_DIR / 'client_secrets.json'
MISSING_CLIENT_SECRETS_MESSAGE = f'''
WARNING: Please configure OAuth 2.0 by downloading client_secrets.json from

  https://console.developers.google.com/apis/credentials?project=YOUR_PROJECT

and putting it at

  {CLIENT_SECRETS_FILE}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
'''


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, **kwargs):
        parents = list(kwargs.get('parents', []))
        parents.append(oauth2client.tools.argparser)
        kwargs['parents'] = parents
        super().__init__(**kwargs)


# youtube_scopes is a list of OAuth scopes with the
# https://www.googleapis.com/auth/ prefix stripped.
#
# In case only a single scope is needed, a single string is allowed in
# place of youtube_scopes, which is automatically understood as a
# singleton list.
#
# Typical scopes:
# - youtube
# - youtube.readonly
# - youtube.upload
# - yt-analytics.readonly
def get_authenticated_http_client(args, youtube_scopes):
    if isinstance(youtube_scopes, str):
        # Singleton
        youtube_scopes = [youtube_scopes]
    flow = oauth2client.client.flow_from_clientsecrets(
        CLIENT_SECRETS_FILE,
        scope=' '.join(f'https://www.googleapis.com/auth/{scope}' for scope in youtube_scopes),
        message=MISSING_CLIENT_SECRETS_MESSAGE,
    )
    oauth_credentials_file = CONFIGS_DIR / f'credentials-{",".join(youtube_scopes)}.json'
    storage = oauth2client.file.Storage(oauth_credentials_file)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = oauth2client.tools.run_flow(flow, storage, args)
    return credentials.authorize(httplib2.Http())


# Typical scopes:
# - youtube
# - youtube.readonly
# - youtube.upload
def get_youtube_client(args, scopes):
    http = get_authenticated_http_client(args, scopes)
    return googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        http=http,
    )


# Typical scopes:
# - yt-analytics.readonly
def get_youtube_analytics_client(args, scopes):
    http = get_authenticated_http_client(args, scopes)
    return googleapiclient.discovery.build(
        YOUTUBE_ANALYTICS_API_SERVICE_NAME,
        YOUTUBE_ANALYTICS_API_VERSION,
        http=http,
    )
