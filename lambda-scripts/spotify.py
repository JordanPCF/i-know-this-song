from secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN
from playlist import Playlist
from song import Song
import requests
# import requests_cache
from typing import Sequence
# import sys
import json
# import functools


SCOPE = "user-library-read%20playlist-read-private%20playlist-read-collaborative%20user-modify-playback-state%20user-read-playback-state"
AUTH_URL = 'https://accounts.spotify.com/api/token'
USER_PLAYLIST_ENDPOINT = 'https://api.spotify.com/v1/me/playlists'#?limit=50'
SAVED_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/me/tracks'
PLAYBACK_QUEUE_ENDPOINT = 'https://api.spotify.com/v1/me/player/queue'
PLAYBACK_DEVICES_ENDPOINT = 'https://api.spotify.com/v1/me/player/devices'

MARKET = 'from_token'

# requests_cache.install_cache('spotify_cache', backend='sqlite', expire_after=99999999999)


def _request_access_token() -> str:
    refresh_params = {'grant_type': 'refresh_token', 'refresh_token': SPOTIFY_REFRESH_TOKEN, 'client_id': SPOTIFY_CLIENT_ID, 'client_secret': SPOTIFY_CLIENT_SECRET}
    refresh_response = requests.post(AUTH_URL, refresh_params).json()

    return refresh_response['access_token']


def _make_request(method: str, endpoint: str, data: dict, json_: bool=True) -> dict:
    latest_access_token = _request_access_token()
    header = {'Authorization': f'Bearer {latest_access_token}'}

    r = requests.request(method, endpoint, params=data, headers=header)
    return r.json() if json else r


def _request_user_playlists(offset=0, limit=50) -> Sequence[dict]:
    all_pages_response = []
    response = _make_request('GET', USER_PLAYLIST_ENDPOINT, {'offset': offset, 'limit': limit})

    while response['next'] is not None:
        all_pages_response.append(response)
        offset += limit
        response = _make_request('GET', USER_PLAYLIST_ENDPOINT, {'offset': offset, 'limit': limit})
    all_pages_response.append(response)

    return all_pages_response


def _request_playlist_songs(playlist: Playlist, offset=0, limit=50) -> Sequence[dict]:
    all_pages_response = []

    PLAYLIST_ITEMS_ENDPOINT = f'https://api.spotify.com/v1/playlists/{playlist.id}/tracks'
    response = _make_request('GET', PLAYLIST_ITEMS_ENDPOINT, {'market': MARKET, 'offset': offset, 'limit': limit})

    while response['next'] is not None:
        all_pages_response.append(response)
        offset += limit
        response = _make_request('GET', PLAYLIST_ITEMS_ENDPOINT, {'market': MARKET, 'offset': offset, 'limit': limit})
    all_pages_response.append(response)

    return all_pages_response


def _request_playback_devices() -> dict:
    return _make_request('GET', PLAYBACK_DEVICES_ENDPOINT, data=None)


def _sanitize_song_title(title: str) -> str:
    # TODO
    return title


def _get_mobile_device_info() -> str:
    device_response = _request_playback_devices()
    for device in device_response['devices']:
        if device['type'] == 'Smartphone':
            return device['id']


# @functools.lru_cache(maxsize=100)
def get_user_playlists() -> Sequence[Playlist]:
    response = _request_user_playlists()

    all_playlists = []
    for page in response:
        for playlist in page['items']:
            if playlist['name'] is not None:
                pl = Playlist(playlist["name"], playlist["id"])
                all_playlists.append(pl)

    return all_playlists


# @functools.lru_cache(maxsize=1000)
def get_playlists_songs(playlist: Playlist) -> Sequence[Song]:
    response = _request_playlist_songs(playlist)
    all_songs = []

    for page in response:
        for song in page["items"]:
            if song['track'] is not None:
                title = _sanitize_song_title(song['track']['name'])
                artist = song['track']['artists'][0]['name']
                uri = song['track']['uri']

                s = Song(title, artist, uri=uri)
                all_songs.append(s)

    return all_songs


def add_song_to_queue(song: Song):
    song_uri = song.uri
    device = _get_mobile_device_info()
    data = {'uri': song_uri, 'device_id': device}

    r = _make_request('POST', PLAYBACK_QUEUE_ENDPOINT, data, json_=False)

    if r.status_code == 204:
        print('Song added to queue!')
    # TODO: add error if device is not active

    
