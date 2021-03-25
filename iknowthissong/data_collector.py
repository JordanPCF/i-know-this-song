from spotify import get_user_playlists, get_playlists_songs, add_song_to_queue
from genius import get_songs_from_lyrics
from typing import Sequence
from song import Song
from playlist import Playlist
import sys
# import requests_cache
import functools

# requests_cache.install_cache('data_collector_cache', backend='sqlite', expire_after=99999999999)

MY_PLAYLISTS = get_user_playlists()
PLAYLIST_DICT = {}
for i, playlist in enumerate(MY_PLAYLISTS):
    PLAYLIST_DICT[i] = playlist

@functools.lru_cache(maxsize=1000)
def get_song_set(playlists: Sequence[Playlist]) -> Sequence[Song]:
    all_songs = []
    for pl in playlists:
        all_songs.extend(get_playlists_songs(pl))
    return set(all_songs)


def make_artist_set(songs: Sequence[Song]) -> Sequence[str]:
    return set([s.artist for s in songs])

PLAYLIST_SONGS = get_song_set([PLAYLIST_DICT[60], PLAYLIST_DICT[15]])