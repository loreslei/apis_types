const express = require('express');
const db = require('../db');

const app = express();
app.use(express.json());

app.get('/users', async (req, res) => {
  try {
    const users = await db.getUsers();
    res.json(users);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/songs', async (req, res) => {
  try {
    const songs = await db.getSongs();
    res.json(songs);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/users/:id/playlists', async (req, res) => {
  try {
    const playlists = await db.getUserPlaylists(req.params.id);
    res.json(playlists);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/playlists/:id/songs', async (req, res) => {
  try {
    const songs = await db.getPlaylistSongs(req.params.id);
    res.json(songs);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/songs/:id/playlists', async (req, res) => {
  try {
    const playlists = await db.getSongPlaylists(req.params.id);
    res.json(playlists);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// CRUD Users
app.post('/users', async (req, res) => {
  try {
    const result = await db.createUser(req.body.name, req.body.age);
    res.json({ success: true, id: result.lastID });
  } catch (err) { res.status(500).json({ error: err.message }); }
});
app.put('/users/:id', async (req, res) => {
  try {
    await db.updateUser(req.params.id, req.body.name, req.body.age);
    res.json({ success: true });
  } catch (err) { res.status(500).json({ error: err.message }); }
});
app.delete('/users/:id', async (req, res) => {
  try {
    await db.deleteUser(req.params.id);
    res.json({ success: true });
  } catch (err) { res.status(500).json({ error: err.message }); }
});

// CRUD Songs
app.post('/songs', async (req, res) => {
  try {
    const result = await db.createSong(req.body.name, req.body.artist);
    res.json({ success: true, id: result.lastID });
  } catch (err) { res.status(500).json({ error: err.message }); }
});
app.put('/songs/:id', async (req, res) => {
  try {
    await db.updateSong(req.params.id, req.body.name, req.body.artist);
    res.json({ success: true });
  } catch (err) { res.status(500).json({ error: err.message }); }
});
app.delete('/songs/:id', async (req, res) => {
  try {
    await db.deleteSong(req.params.id);
    res.json({ success: true });
  } catch (err) { res.status(500).json({ error: err.message }); }
});

// CRUD Playlists
app.post('/playlists', async (req, res) => {
  try {
    const result = await db.createPlaylist(req.body.name, req.body.userId);
    res.json({ success: true, id: result.lastID });
  } catch (err) { res.status(500).json({ error: err.message }); }
});
app.put('/playlists/:id', async (req, res) => {
  try {
    await db.updatePlaylist(req.params.id, req.body.name);
    res.json({ success: true });
  } catch (err) { res.status(500).json({ error: err.message }); }
});
app.delete('/playlists/:id', async (req, res) => {
  try {
    await db.deletePlaylist(req.params.id);
    res.json({ success: true });
  } catch (err) { res.status(500).json({ error: err.message }); }
});

// CRUD Playlist Songs
app.post('/playlists/:id/songs', async (req, res) => {
  try {
    await db.addSongToPlaylist(req.params.id, req.body.songId);
    res.json({ success: true });
  } catch (err) { res.status(500).json({ error: err.message }); }
});
app.delete('/playlists/:id/songs/:songId', async (req, res) => {
  try {
    await db.removeSongFromPlaylist(req.params.id, req.params.songId);
    res.json({ success: true });
  } catch (err) { res.status(500).json({ error: err.message }); }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Node REST API running on port ${PORT}`);
});
