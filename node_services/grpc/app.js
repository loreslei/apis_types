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
