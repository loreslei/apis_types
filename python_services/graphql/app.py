import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import sys
import os

# Add parent directory to path to import db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db

@strawberry.type
class User:
    id: int
    name: str
    age: int

@strawberry.type
class Song:
    id: int
    name: str
    artist: str

@strawberry.type
class Playlist:
    id: int
    name: str
    user_id: int

@strawberry.type
class Query:
    @strawberry.field
    def get_users(self) -> list[User]:
        return [User(**row) for row in db.get_users()]

    @strawberry.field
    def get_songs(self) -> list[Song]:
        return [Song(**row) for row in db.get_songs()]

    @strawberry.field
    def get_user_playlists(self, user_id: int) -> list[Playlist]:
        return [Playlist(**row) for row in db.get_user_playlists(user_id)]

    @strawberry.field
    def get_playlist_songs(self, playlist_id: int) -> list[Song]:
        return [Song(**row) for row in db.get_playlist_songs(playlist_id)]

    @strawberry.field
    def get_song_playlists(self, song_id: int) -> list[Playlist]:
        return [Playlist(**row) for row in db.get_song_playlists(song_id)]

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
