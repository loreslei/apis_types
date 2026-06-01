import sqlite3
import random
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite')

def generate_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            artist TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    c.execute('''
        CREATE TABLE playlist_songs (
            playlist_id INTEGER NOT NULL,
            song_id INTEGER NOT NULL,
            PRIMARY KEY (playlist_id, song_id),
            FOREIGN KEY (playlist_id) REFERENCES playlists (id),
            FOREIGN KEY (song_id) REFERENCES songs (id)
        )
    ''')

    # Seed data
    print("Generating data...")
    num_users = 1000
    num_songs = 5000
    num_playlists = 2000

    users = []
    for i in range(num_users):
        users.append((f"User_{i}", random.randint(12, 80)))
    
    c.executemany('INSERT INTO users (name, age) VALUES (?, ?)', users)

    songs = []
    for i in range(num_songs):
        songs.append((f"Song_{i}", f"Artist_{i % 500}"))
    
    c.executemany('INSERT INTO songs (name, artist) VALUES (?, ?)', songs)

    playlists = []
    for i in range(num_playlists):
        user_id = random.randint(1, num_users)
        playlists.append((f"Playlist_{i}", user_id))
    
    c.executemany('INSERT INTO playlists (name, user_id) VALUES (?, ?)', playlists)

    playlist_songs = set()
    for _ in range(15000): # ~15000 associations
        playlist_id = random.randint(1, num_playlists)
        song_id = random.randint(1, num_songs)
        playlist_songs.add((playlist_id, song_id))

    c.executemany('INSERT INTO playlist_songs (playlist_id, song_id) VALUES (?, ?)', list(playlist_songs))

    conn.commit()
    conn.close()
    print("Database created successfully at", DB_PATH)

if __name__ == '__main__':
    generate_db()
