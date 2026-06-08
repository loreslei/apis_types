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

    def CreateUser(self, request, context):
        db.create_user(request.name, request.age)
        return music_pb2.MutationResponse(success=True, message="Created")

    def UpdateUser(self, request, context):
        db.update_user(request.id, request.name, request.age)
        return music_pb2.MutationResponse(success=True, message="Updated")

    def DeleteUser(self, request, context):
        db.delete_user(request.id)
        return music_pb2.MutationResponse(success=True, message="Deleted")

    def CreateSong(self, request, context):
        db.create_song(request.name, request.artist)
        return music_pb2.MutationResponse(success=True, message="Created")

    def UpdateSong(self, request, context):
        db.update_song(request.id, request.name, request.artist)
        return music_pb2.MutationResponse(success=True, message="Updated")

    def DeleteSong(self, request, context):
        db.delete_song(request.id)
        return music_pb2.MutationResponse(success=True, message="Deleted")

    def CreatePlaylist(self, request, context):
        db.create_playlist(request.name, request.user_id)
        return music_pb2.MutationResponse(success=True, message="Created")

    def UpdatePlaylist(self, request, context):
        db.update_playlist(request.id, request.name)
        return music_pb2.MutationResponse(success=True, message="Updated")

    def DeletePlaylist(self, request, context):
        db.delete_playlist(request.id)
        return music_pb2.MutationResponse(success=True, message="Deleted")

    def AddSongToPlaylist(self, request, context):
        db.add_song_to_playlist(request.playlist_id, request.song_id)
        return music_pb2.MutationResponse(success=True, message="Added")

    def RemoveSongFromPlaylist(self, request, context):
        db.remove_song_from_playlist(request.playlist_id, request.song_id)
        return music_pb2.MutationResponse(success=True, message="Removed")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    music_pb2_grpc.add_MusicServiceServicer_to_server(MusicService(), server)
    server.add_insecure_port('[::]:8003')
    print("Python gRPC API running on port 8003")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
