const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const db = require('../db');

const PROTO_PATH = path.join(__dirname, '..', '..', 'db', 'music.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const musicProto = grpc.loadPackageDefinition(packageDefinition).music;

const server = new grpc.Server();

server.addService(musicProto.MusicService.service, {
  GetUsers: async (_, callback) => {
    try {
      const users = await db.getUsers();
      callback(null, { users });
    } catch (error) {
      callback(error, null);
    }
  },
  GetSongs: async (_, callback) => {
    try {
      const songs = await db.getSongs();
      callback(null, { songs });
    } catch (error) {
      callback(error, null);
    }
  },
  GetUserPlaylists: async (call, callback) => {
    try {
      const playlists = await db.getUserPlaylists(call.request.id);
      callback(null, { playlists });
    } catch (error) {
      callback(error, null);
    }
  },
  GetPlaylistSongs: async (call, callback) => {
    try {
      const songs = await db.getPlaylistSongs(call.request.id);
      callback(null, { songs });
    } catch (error) {
      callback(error, null);
    }
  },
  GetSongPlaylists: async (call, callback) => {
    try {
      const playlists = await db.getSongPlaylists(call.request.id);
      callback(null, { playlists });
    } catch (error) {
      callback(error, null);
    }
  },

  CreateUser: async (call, callback) => {
    try {
      await db.createUser(call.request.name, call.request.age);
      callback(null, { success: true, message: "Created" });
    } catch (error) { callback(error, null); }
  },
  UpdateUser: async (call, callback) => {
    try {
      await db.updateUser(call.request.id, call.request.name, call.request.age);
      callback(null, { success: true, message: "Updated" });
    } catch (error) { callback(error, null); }
  },
  DeleteUser: async (call, callback) => {
    try {
      await db.deleteUser(call.request.id);
      callback(null, { success: true, message: "Deleted" });
    } catch (error) { callback(error, null); }
  },

  CreateSong: async (call, callback) => {
    try {
      await db.createSong(call.request.name, call.request.artist);
      callback(null, { success: true, message: "Created" });
    } catch (error) { callback(error, null); }
  },
  UpdateSong: async (call, callback) => {
    try {
      await db.updateSong(call.request.id, call.request.name, call.request.artist);
      callback(null, { success: true, message: "Updated" });
    } catch (error) { callback(error, null); }
  },
  DeleteSong: async (call, callback) => {
    try {
      await db.deleteSong(call.request.id);
      callback(null, { success: true, message: "Deleted" });
    } catch (error) { callback(error, null); }
  },

  CreatePlaylist: async (call, callback) => {
    try {
      await db.createPlaylist(call.request.name, call.request.user_id);
      callback(null, { success: true, message: "Created" });
    } catch (error) { callback(error, null); }
  },
  UpdatePlaylist: async (call, callback) => {
    try {
      await db.updatePlaylist(call.request.id, call.request.name);
      callback(null, { success: true, message: "Updated" });
    } catch (error) { callback(error, null); }
  },
  DeletePlaylist: async (call, callback) => {
    try {
      await db.deletePlaylist(call.request.id);
      callback(null, { success: true, message: "Deleted" });
    } catch (error) { callback(error, null); }
  },

  AddSongToPlaylist: async (call, callback) => {
    try {
      await db.addSongToPlaylist(call.request.playlist_id, call.request.song_id);
      callback(null, { success: true, message: "Added" });
    } catch (error) { callback(error, null); }
  },
  RemoveSongFromPlaylist: async (call, callback) => {
    try {
      await db.removeSongFromPlaylist(call.request.playlist_id, call.request.song_id);
      callback(null, { success: true, message: "Removed" });
    } catch (error) { callback(error, null); }
  }
});

const PORT = 3003;
server.bindAsync(`0.0.0.0:${PORT}`, grpc.ServerCredentials.createInsecure(), (err, port) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log(`Node gRPC API running on port ${port}`);
  server.start();
});
