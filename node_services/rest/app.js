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

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Node REST API running on port ${PORT}`);
});
