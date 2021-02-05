from secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN
from playlist import Playlist
from song import Song
import requests
from typing import Sequence
# import json


SCOPE = "user-library-read%20playlist-read-private%20playlist-read-collaborative"
AUTH_URL = 'https://accounts.spotify.com/api/token'
USER_PLAYLIST_ENDPOINT = 'https://api.spotify.com/v1/me/playlists?limit=50'
SAVED_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/me/tracks'

MARKET = 'from_token'


def _request_access_token() -> str:
    refresh_params = {'grant_type': 'refresh_token', 'refresh_token': SPOTIFY_REFRESH_TOKEN, 'client_id': SPOTIFY_CLIENT_ID, 'client_secret': SPOTIFY_CLIENT_SECRET}
    refresh_response = requests.post(AUTH_URL, refresh_params).json()

    return refresh_response['access_token']


def _request_user_playlists(offset=0, limit=50) -> dict:
    latest_access_token = _request_access_token()
    data = {'offset': offset, 'limit': limit}
    header = {'Authorization': f'Bearer {latest_access_token}'}
    user_playlists_response = requests.get(USER_PLAYLIST_ENDPOINT, params=data, headers=header).json()
    return user_playlists_response


def _request_playlist_songs(id, offset=0, limit=100) -> Sequence[dict]:
    all_pages = []

    PLAYLIST_ITEMS_ENDPOINT = f'https://api.spotify.com/v1/playlists/{id}/tracks'
    latest_access_token = _request_access_token()
    data = {'offset': offset, 'limit': limit}
    header = {'Authorization': f'Bearer {latest_access_token}'}

    playlists_song_response = requests.get(PLAYLIST_ITEMS_ENDPOINT, params=data, headers=header).json()
    # TODO get another page of results
    all_pages.append(playlists_song_response)

    return all_pages


def _get_playlist_info(json_response) -> Sequence[Playlist]:
    all_playlists = []

    for playlist in json_response['items']:
        playlist_name = playlist["name"]
        playlist_id = playlist["id"]
        num_tracks = playlist["tracks"]["total"]

        pl = Playlist(playlist_name, playlist_id, num_tracks)

        all_playlists.append(pl)


def _sanitize_song_title(title: str) -> str:
    # TODO
    return title


def get_playlists_songs(json_response: Sequence[dict]) -> Sequence[Song]:
    all_songs = []

    for response in json_response:
        for song in response["items"]:
            title = _sanitize_song_title(song['track']['name'])
            artist = song['track']['artists'][0]['name']

            s = Song(title, artist)
            all_songs.append(s)

    return all_songs






# test_app_id = '1zRPWN73G2REOoMJoXjwKy'
# print(get_playlists_songs(_request_playlist_songs(test_app_id)))

    
