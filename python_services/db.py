import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'database.sqlite')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    return [dict(row) for row in c.fetchall()]

def get_songs():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM songs')
    return [dict(row) for row in c.fetchall()]

def get_user_playlists(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM playlists WHERE user_id = ?', (user_id,))
    return [dict(row) for row in c.fetchall()]

def get_playlist_songs(playlist_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT s.* FROM songs s
        JOIN playlist_songs ps ON s.id = ps.song_id
        WHERE ps.playlist_id = ?
    ''', (playlist_id,))
    return [dict(row) for row in c.fetchall()]

def get_song_playlists(song_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT p.* FROM playlists p
        JOIN playlist_songs ps ON p.id = ps.playlist_id
        WHERE ps.song_id = ?
    ''', (song_id,))
    return [dict(row) for row in c.fetchall()]

def run_query(sql, params=()):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(sql, params)
    conn.commit()
    result = {'lastrowid': c.lastrowid, 'rowcount': c.rowcount}
    conn.close()
    return result

# CRUD for Users
def create_user(name, age):
    return run_query('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))

def update_user(id, name, age):
    return run_query('UPDATE users SET name = ?, age = ? WHERE id = ?', (name, age, id))

def delete_user(id):
    return run_query('DELETE FROM users WHERE id = ?', (id,))

# CRUD for Songs
def create_song(name, artist):
    return run_query('INSERT INTO songs (name, artist) VALUES (?, ?)', (name, artist))

def update_song(id, name, artist):
    return run_query('UPDATE songs SET name = ?, artist = ? WHERE id = ?', (name, artist, id))

def delete_song(id):
    return run_query('DELETE FROM songs WHERE id = ?', (id,))

# CRUD for Playlists
def create_playlist(name, user_id):
    return run_query('INSERT INTO playlists (name, user_id) VALUES (?, ?)', (name, user_id))

def update_playlist(id, name):
    return run_query('UPDATE playlists SET name = ? WHERE id = ?', (name, id))

def delete_playlist(id):
    return run_query('DELETE FROM playlists WHERE id = ?', (id,))

# CRUD for Playlist Songs
def add_song_to_playlist(playlist_id, song_id):
    return run_query('INSERT INTO playlist_songs (playlist_id, song_id) VALUES (?, ?)', (playlist_id, song_id))

def remove_song_from_playlist(playlist_id, song_id):
    return run_query('DELETE FROM playlist_songs WHERE playlist_id = ? AND song_id = ?', (playlist_id, song_id))

