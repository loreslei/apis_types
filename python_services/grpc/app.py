import grpc
from concurrent import futures
import sys
import os

# Add parent directory to path to import db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db

import music_pb2
import music_pb2_grpc

class MusicService(music_pb2_grpc.MusicServiceServicer):
    def GetUsers(self, request, context):
        users = [music_pb2.User(**row) for row in db.get_users()]
        return music_pb2.UserList(users=users)

    def GetSongs(self, request, context):
        songs = [music_pb2.Song(**row) for row in db.get_songs()]
        return music_pb2.SongList(songs=songs)

    def GetUserPlaylists(self, request, context):
        playlists = [music_pb2.Playlist(**row) for row in db.get_user_playlists(request.id)]
        return music_pb2.PlaylistList(playlists=playlists)

    def GetPlaylistSongs(self, request, context):
        songs = [music_pb2.Song(**row) for row in db.get_playlist_songs(request.id)]
        return music_pb2.SongList(songs=songs)

    def GetSongPlaylists(self, request, context):
        playlists = [music_pb2.Playlist(**row) for row in db.get_song_playlists(request.id)]
        return music_pb2.PlaylistList(playlists=playlists)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    music_pb2_grpc.add_MusicServiceServicer_to_server(MusicService(), server)
    server.add_insecure_port('[::]:8003')
    print("Python gRPC API running on port 8003")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
