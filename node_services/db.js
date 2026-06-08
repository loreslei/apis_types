const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.join(__dirname, '..', 'db', 'database.sqlite');
const db = new sqlite3.Database(dbPath);

// Helper function to query multiple rows
const queryAll = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.all(sql, params, (err, rows) => {
      if (err) reject(err);
      else resolve(rows);
    });
  });
};

// Helper function to run insert/update/delete operations
const runQuery = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.run(sql, params, function(err) {
      if (err) reject(err);
      else resolve({ lastID: this.lastID, changes: this.changes });
    });
  });
};

module.exports = {
  db,
  
  getUsers: () => queryAll('SELECT * FROM users'),
  
  getSongs: () => queryAll('SELECT * FROM songs'),
  
  getUserPlaylists: (userId) => queryAll('SELECT * FROM playlists WHERE user_id = ?', [userId]),
  
  getPlaylistSongs: (playlistId) => {
    return queryAll(`
      SELECT s.* FROM songs s
      JOIN playlist_songs ps ON s.id = ps.song_id
      WHERE ps.playlist_id = ?
    `, [playlistId]);
  },
  
  getSongPlaylists: (songId) => {
    return queryAll(`
      SELECT p.* FROM playlists p
      JOIN playlist_songs ps ON p.id = ps.playlist_id
      WHERE ps.song_id = ?
    `, [songId]);
  },

  // CRUD for Users
  createUser: (name, age) => runQuery('INSERT INTO users (name, age) VALUES (?, ?)', [name, age]),
  updateUser: (id, name, age) => runQuery('UPDATE users SET name = ?, age = ? WHERE id = ?', [name, age, id]),
  deleteUser: (id) => runQuery('DELETE FROM users WHERE id = ?', [id]),

  // CRUD for Songs
  createSong: (name, artist) => runQuery('INSERT INTO songs (name, artist) VALUES (?, ?)', [name, artist]),
  updateSong: (id, name, artist) => runQuery('UPDATE songs SET name = ?, artist = ? WHERE id = ?', [name, artist, id]),
  deleteSong: (id) => runQuery('DELETE FROM songs WHERE id = ?', [id]),

  // CRUD for Playlists
  createPlaylist: (name, userId) => runQuery('INSERT INTO playlists (name, user_id) VALUES (?, ?)', [name, userId]),
  updatePlaylist: (id, name) => runQuery('UPDATE playlists SET name = ? WHERE id = ?', [name, id]),
  deletePlaylist: (id) => runQuery('DELETE FROM playlists WHERE id = ?', [id]),

  // CRUD for Playlist Songs
  addSongToPlaylist: (playlistId, songId) => runQuery('INSERT INTO playlist_songs (playlist_id, song_id) VALUES (?, ?)', [playlistId, songId]),
  removeSongFromPlaylist: (playlistId, songId) => runQuery('DELETE FROM playlist_songs WHERE playlist_id = ? AND song_id = ?', [playlistId, songId])
};
