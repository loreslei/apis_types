from fastapi import FastAPI
import sys
import os

# Add parent directory to path to import db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db

app = FastAPI()

@app.get("/users")
def get_users():
    return db.get_users()

@app.get("/songs")
def get_songs():
    return db.get_songs()

@app.get("/users/{user_id}/playlists")
def get_user_playlists(user_id: int):
    return db.get_user_playlists(user_id)

@app.get("/playlists/{playlist_id}/songs")
def get_playlist_songs(playlist_id: int):
    return db.get_playlist_songs(playlist_id)

@app.get("/songs/{song_id}/playlists")
def get_song_playlists(song_id: int):
    return db.get_song_playlists(song_id)

from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    age: int

class SongCreate(BaseModel):
    name: str
    artist: str

class PlaylistCreate(BaseModel):
    name: str
    userId: int

class PlaylistSongAdd(BaseModel):
    songId: int

# CRUD Users
@app.post("/users")
def create_user(user: UserCreate):
    res = db.create_user(user.name, user.age)
    return {"success": True, "id": res['lastrowid']}

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate):
    db.update_user(user_id, user.name, user.age)
    return {"success": True}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db.delete_user(user_id)
    return {"success": True}

# CRUD Songs
@app.post("/songs")
def create_song(song: SongCreate):
    res = db.create_song(song.name, song.artist)
    return {"success": True, "id": res['lastrowid']}

@app.put("/songs/{song_id}")
def update_song(song_id: int, song: SongCreate):
    db.update_song(song_id, song.name, song.artist)
    return {"success": True}

@app.delete("/songs/{song_id}")
def delete_song(song_id: int):
    db.delete_song(song_id)
    return {"success": True}

# CRUD Playlists
@app.post("/playlists")
def create_playlist(playlist: PlaylistCreate):
    res = db.create_playlist(playlist.name, playlist.userId)
    return {"success": True, "id": res['lastrowid']}

@app.put("/playlists/{playlist_id}")
def update_playlist(playlist_id: int, playlist: PlaylistCreate):
    db.update_playlist(playlist_id, playlist.name)
    return {"success": True}

@app.delete("/playlists/{playlist_id}")
def delete_playlist(playlist_id: int):
    db.delete_playlist(playlist_id)
    return {"success": True}

# CRUD Playlist Songs
@app.post("/playlists/{playlist_id}/songs")
def add_song_to_playlist(playlist_id: int, data: PlaylistSongAdd):
    db.add_song_to_playlist(playlist_id, data.songId)
    return {"success": True}

@app.delete("/playlists/{playlist_id}/songs/{song_id}")
def remove_song_from_playlist(playlist_id: int, song_id: int):
    db.remove_song_from_playlist(playlist_id, song_id)
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
