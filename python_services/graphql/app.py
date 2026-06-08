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

@strawberry.type
class MutationResponse:
    success: bool
    message: str | None = None
    id: int | None = None

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str, age: int) -> MutationResponse:
        res = db.create_user(name, age)
        return MutationResponse(success=True, id=res['lastrowid'])

    @strawberry.mutation
    def update_user(self, id: int, name: str, age: int) -> MutationResponse:
        db.update_user(id, name, age)
        return MutationResponse(success=True)

    @strawberry.mutation
    def delete_user(self, id: int) -> MutationResponse:
        db.delete_user(id)
        return MutationResponse(success=True)

    @strawberry.mutation
    def create_song(self, name: str, artist: str) -> MutationResponse:
        res = db.create_song(name, artist)
        return MutationResponse(success=True, id=res['lastrowid'])

    @strawberry.mutation
    def update_song(self, id: int, name: str, artist: str) -> MutationResponse:
        db.update_song(id, name, artist)
        return MutationResponse(success=True)

    @strawberry.mutation
    def delete_song(self, id: int) -> MutationResponse:
        db.delete_song(id)
        return MutationResponse(success=True)

    @strawberry.mutation
    def create_playlist(self, name: str, user_id: int) -> MutationResponse:
        res = db.create_playlist(name, user_id)
        return MutationResponse(success=True, id=res['lastrowid'])

    @strawberry.mutation
    def update_playlist(self, id: int, name: str) -> MutationResponse:
        db.update_playlist(id, name)
        return MutationResponse(success=True)

    @strawberry.mutation
    def delete_playlist(self, id: int) -> MutationResponse:
        db.delete_playlist(id)
        return MutationResponse(success=True)

    @strawberry.mutation
    def add_song_to_playlist(self, playlist_id: int, song_id: int) -> MutationResponse:
        db.add_song_to_playlist(playlist_id, song_id)
        return MutationResponse(success=True)

    @strawberry.mutation
    def remove_song_from_playlist(self, playlist_id: int, song_id: int) -> MutationResponse:
        db.remove_song_from_playlist(playlist_id, song_id)
        return MutationResponse(success=True)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
