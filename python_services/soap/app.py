import sys
import os

# Add parent directory to path to import db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db

from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, ComplexModel, Array, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class User(ComplexModel):
    id = Integer
    name = Unicode
    age = Integer

class Song(ComplexModel):
    id = Integer
    name = Unicode
    artist = Unicode

class Playlist(ComplexModel):
    id = Integer
    name = Unicode
    userId = Integer

class MutationResponse(ComplexModel):
    success = Boolean
    message = Unicode
    id = Integer

class MusicService(ServiceBase):
    @rpc(_returns=Array(User))
    def GetUsers(ctx):
        users = db.get_users()
        return [User(id=u['id'], name=u['name'], age=u['age']) for u in users]

    @rpc(_returns=Array(Song))
    def GetSongs(ctx):
        songs = db.get_songs()
        return [Song(id=s['id'], name=s['name'], artist=s['artist']) for s in songs]

    @rpc(Integer, _returns=Array(Playlist))
    def GetUserPlaylists(ctx, id):
        playlists = db.get_user_playlists(id)
        return [Playlist(id=p['id'], name=p['name'], userId=p['user_id']) for p in playlists]

    @rpc(Integer, _returns=Array(Song))
    def GetPlaylistSongs(ctx, id):
        songs = db.get_playlist_songs(id)
        return [Song(id=s['id'], name=s['name'], artist=s['artist']) for s in songs]

    @rpc(Integer, _returns=Array(Playlist))
    def GetSongPlaylists(ctx, id):
        playlists = db.get_song_playlists(id)
        return [Playlist(id=p['id'], name=p['name'], userId=p['user_id']) for p in playlists]

    @rpc(Unicode, Integer, _returns=MutationResponse)
    def CreateUser(ctx, name, age):
        res = db.create_user(name, age)
        return MutationResponse(success=True, message="Created", id=res['lastrowid'])

    @rpc(Integer, Unicode, Integer, _returns=MutationResponse)
    def UpdateUser(ctx, id, name, age):
        db.update_user(id, name, age)
        return MutationResponse(success=True, message="Updated")

    @rpc(Integer, _returns=MutationResponse)
    def DeleteUser(ctx, id):
        db.delete_user(id)
        return MutationResponse(success=True, message="Deleted")

    @rpc(Unicode, Unicode, _returns=MutationResponse)
    def CreateSong(ctx, name, artist):
        res = db.create_song(name, artist)
        return MutationResponse(success=True, message="Created", id=res['lastrowid'])

    @rpc(Integer, Unicode, Unicode, _returns=MutationResponse)
    def UpdateSong(ctx, id, name, artist):
        db.update_song(id, name, artist)
        return MutationResponse(success=True, message="Updated")

    @rpc(Integer, _returns=MutationResponse)
    def DeleteSong(ctx, id):
        db.delete_song(id)
        return MutationResponse(success=True, message="Deleted")

    @rpc(Unicode, Integer, _returns=MutationResponse)
    def CreatePlaylist(ctx, name, userId):
        res = db.create_playlist(name, userId)
        return MutationResponse(success=True, message="Created", id=res['lastrowid'])

    @rpc(Integer, Unicode, _returns=MutationResponse)
    def UpdatePlaylist(ctx, id, name):
        db.update_playlist(id, name)
        return MutationResponse(success=True, message="Updated")

    @rpc(Integer, _returns=MutationResponse)
    def DeletePlaylist(ctx, id):
        db.delete_playlist(id)
        return MutationResponse(success=True, message="Deleted")

    @rpc(Integer, Integer, _returns=MutationResponse)
    def AddSongToPlaylist(ctx, playlistId, songId):
        db.add_song_to_playlist(playlistId, songId)
        return MutationResponse(success=True, message="Added")

    @rpc(Integer, Integer, _returns=MutationResponse)
    def RemoveSongFromPlaylist(ctx, playlistId, songId):
        db.remove_song_from_playlist(playlistId, songId)
        return MutationResponse(success=True, message="Removed")

application = Application([MusicService], 'http://example.com/music',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    from fastapi import FastAPI
    from fastapi.middleware.wsgi import WSGIMiddleware
    import uvicorn
    
    fastapi_app = FastAPI()
    fastapi_app.mount("/", WSGIMiddleware(wsgi_app))
    
    print("Python SOAP API running on port 8004 (concurrent mode)")
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8004)
