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
      },
      CreateUser: async function(args, callback) {
        try {
          await db.createUser(args.name, args.age);
          callback({ success: true, message: "Created" });
        } catch(e) { callback(e); }
      },
      UpdateUser: async function(args, callback) {
        try {
          await db.updateUser(args.id, args.name, args.age);
          callback({ success: true, message: "Updated" });
        } catch(e) { callback(e); }
      },
      DeleteUser: async function(args, callback) {
        try {
          await db.deleteUser(args.id);
          callback({ success: true, message: "Deleted" });
        } catch(e) { callback(e); }
      },
      CreateSong: async function(args, callback) {
        try {
          await db.createSong(args.name, args.artist);
          callback({ success: true, message: "Created" });
        } catch(e) { callback(e); }
      },
      UpdateSong: async function(args, callback) {
        try {
          await db.updateSong(args.id, args.name, args.artist);
          callback({ success: true, message: "Updated" });
        } catch(e) { callback(e); }
      },
      DeleteSong: async function(args, callback) {
        try {
          await db.deleteSong(args.id);
          callback({ success: true, message: "Deleted" });
        } catch(e) { callback(e); }
      },
      CreatePlaylist: async function(args, callback) {
        try {
          await db.createPlaylist(args.name, args.userId);
          callback({ success: true, message: "Created" });
        } catch(e) { callback(e); }
      },
      UpdatePlaylist: async function(args, callback) {
        try {
          await db.updatePlaylist(args.id, args.name);
          callback({ success: true, message: "Updated" });
        } catch(e) { callback(e); }
      },
      DeletePlaylist: async function(args, callback) {
        try {
          await db.deletePlaylist(args.id);
          callback({ success: true, message: "Deleted" });
        } catch(e) { callback(e); }
      },
      AddSongToPlaylist: async function(args, callback) {
        try {
          await db.addSongToPlaylist(args.playlistId, args.songId);
          callback({ success: true, message: "Added" });
        } catch(e) { callback(e); }
      },
      RemoveSongFromPlaylist: async function(args, callback) {
        try {
          await db.removeSongFromPlaylist(args.playlistId, args.songId);
          callback({ success: true, message: "Removed" });
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
