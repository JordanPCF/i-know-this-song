# from spotify import add_song_to_queue
from genius import get_songs_from_lyrics
# from typing import Sequence
# from song import Song
# from playlist import Playlist
# import sys
from data_collector import PLAYLIST_SONGS
print(PLAYLIST_SONGS)


def find_song_in_playlist(lyrics:str):
    search_page = 1
    song_found = False
    song_counter = 0
    while not song_found:
        genius_songs = get_songs_from_lyrics(lyrics, search_page)
        for song in genius_songs:
            song_counter += 1
            if song in PLAYLIST_SONGS:
                song_found = True
                print('Found song! #', song_counter, song)
                return song
            if song_counter % 20 == 0 or song_counter > 980:
                print(song_counter)

        search_page += 1


print(find_song_in_playlist('too busy dreaming'))




