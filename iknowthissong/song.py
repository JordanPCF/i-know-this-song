class Song():

    def __init__(self, title, artist, lyric_snippet="", uri=""):
        self.title = title
        self.artist = artist
        self.lyric_snippet = lyric_snippet
        self.uri = uri # for playback

    def __repr__(self):
        return f'{self.title} by {self.artist}'

    def __eq__(self, obj):
        return (
            isinstance(obj, Song) and
            obj.title == self.title and
            obj.artist == self.artist
        )

    def __hash__(self):
        return hash(repr(self))
