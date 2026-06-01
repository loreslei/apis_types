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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
