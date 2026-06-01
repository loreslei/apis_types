import sys
import os

# Add parent directory to path to import db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db

from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, ComplexModel, Array
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
