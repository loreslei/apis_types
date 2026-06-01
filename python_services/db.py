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
