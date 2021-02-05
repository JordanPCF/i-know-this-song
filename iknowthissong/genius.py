# from secrets import GENIUS_CLIENT_ID
from song import Song
import requests
# import json
from typing import Sequence

LYRIC_ENDPOINT = 'https://genius.com/api/search/lyric'


def lyric_search(lyrics: str, page: int=1, per_page: int=5) -> dict:
    r = requests.get(LYRIC_ENDPOINT, params={'q': lyrics, 'page': page, 'per_page': per_page})
    return r.json()


def _get_next_page():
    pass


def _json_to_songs(json_response: dict) -> Sequence[Song]:
    song_matches = []
    search_hits = json_response['response']['sections'][0]['hits']

    for hit in search_hits:
        if hit['type'] == 'song':
            title = _get_song_title(hit)
            artist = _get_primary_artist(hit)
            lyric_snippet = _get_lyric_snippet(hit)

            song = Song(title, artist, lyric_snippet)
            song_matches.append(song)

    return song_matches


def _get_song_title(hit: dict) -> str:
    #### want title_with_featured?
    return hit['result']['title']


def _get_primary_artist(hit: dict) -> str:
    return hit['result']['primary_artist']['name']


def _get_lyric_snippet(hit: dict) -> str:
    highlight = hit['highlights'][0]
    if highlight['property'] == 'lyric' and highlight['snippet']:
        return highlight['value']


print(_json_to_songs(lyric_search('party girls', per_page=3)))


