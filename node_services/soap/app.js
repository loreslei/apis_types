const soap = require('soap');
const express = require('express');
const fs = require('fs');
const path = require('path');
const db = require('../db');

const service = {
  MusicService: {
    MusicPort: {
      GetUsers: async function(args, callback) {
        try {
          const users = await db.getUsers();
          callback({ users: { user: users } });
        } catch(e) { callback(e); }
      },
      GetSongs: async function(args, callback) {
        try {
          const songs = await db.getSongs();
          callback({ songs: { song: songs } });
        } catch(e) { callback(e); }
      },
      GetUserPlaylists: async function(args, callback) {
        try {
          const playlists = await db.getUserPlaylists(args.id);
          callback({ playlists: { playlist: playlists } });
        } catch(e) { callback(e); }
      },
      GetPlaylistSongs: async function(args, callback) {
        try {
          const songs = await db.getPlaylistSongs(args.id);
          callback({ songs: { song: songs } });
        } catch(e) { callback(e); }
      },
      GetSongPlaylists: async function(args, callback) {
        try {
          const playlists = await db.getSongPlaylists(args.id);
          callback({ playlists: { playlist: playlists } });
        } catch(e) { callback(e); }
      }
    }
  }
};

const xml = fs.readFileSync(path.join(__dirname, '..', '..', 'db', 'music.wsdl'), 'utf8');

const app = express();
const PORT = 3004;

app.listen(PORT, function() {
  soap.listen(app, '/music', service, xml, function() {
    console.log(`Node SOAP API running on port ${PORT}`);
  });
});
