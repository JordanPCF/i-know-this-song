class Playlist():

    def __init__(self, name, id, num_tracks):
        self.name = name
        self.id = id
        self.num_tracks = num_tracks


    def __repr__(self):
        return f'{self.name}:   {self.id}'