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
  }
};
