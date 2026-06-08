const { ApolloServer, gql } = require('apollo-server');
const db = require('../db');

const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    age: Int!
  }

  type Song {
    id: ID!
    name: String!
    artist: String!
  }

  type Playlist {
    id: ID!
    name: String!
    userId: Int!
  }

  type Query {
    getUsers: [User]
    getSongs: [Song]
    getUserPlaylists(userId: ID!): [Playlist]
    getPlaylistSongs(playlistId: ID!): [Song]
    getSongPlaylists(songId: ID!): [Playlist]
  }
  type MutationResponse {
    success: Boolean!
    message: String
    id: ID
  }

  type Mutation {
    createUser(name: String!, age: Int!): MutationResponse!
    updateUser(id: ID!, name: String!, age: Int!): MutationResponse!
    deleteUser(id: ID!): MutationResponse!

    createSong(name: String!, artist: String!): MutationResponse!
    updateSong(id: ID!, name: String!, artist: String!): MutationResponse!
    deleteSong(id: ID!): MutationResponse!

    createPlaylist(name: String!, userId: Int!): MutationResponse!
    updatePlaylist(id: ID!, name: String!): MutationResponse!
    deletePlaylist(id: ID!): MutationResponse!

    addSongToPlaylist(playlistId: Int!, songId: Int!): MutationResponse!
    removeSongFromPlaylist(playlistId: Int!, songId: Int!): MutationResponse!
  }
`;

const resolvers = {
  Query: {
    getUsers: () => db.getUsers(),
    getSongs: () => db.getSongs(),
    getUserPlaylists: (_, { userId }) => db.getUserPlaylists(userId),
    getPlaylistSongs: (_, { playlistId }) => db.getPlaylistSongs(playlistId),
    getSongPlaylists: (_, { songId }) => db.getSongPlaylists(songId),
  },
  Mutation: {
    createUser: async (_, { name, age }) => {
      const res = await db.createUser(name, age);
      return { success: true, id: res.lastID };
    },
    updateUser: async (_, { id, name, age }) => {
      await db.updateUser(id, name, age);
      return { success: true };
    },
    deleteUser: async (_, { id }) => {
      await db.deleteUser(id);
      return { success: true };
    },
    createSong: async (_, { name, artist }) => {
      const res = await db.createSong(name, artist);
      return { success: true, id: res.lastID };
    },
    updateSong: async (_, { id, name, artist }) => {
      await db.updateSong(id, name, artist);
      return { success: true };
    },
    deleteSong: async (_, { id }) => {
      await db.deleteSong(id);
      return { success: true };
    },
    createPlaylist: async (_, { name, userId }) => {
      const res = await db.createPlaylist(name, userId);
      return { success: true, id: res.lastID };
    },
    updatePlaylist: async (_, { id, name }) => {
      await db.updatePlaylist(id, name);
      return { success: true };
    },
    deletePlaylist: async (_, { id }) => {
      await db.deletePlaylist(id);
      return { success: true };
    },
    addSongToPlaylist: async (_, { playlistId, songId }) => {
      await db.addSongToPlaylist(playlistId, songId);
      return { success: true };
    },
    removeSongFromPlaylist: async (_, { playlistId, songId }) => {
      await db.removeSongFromPlaylist(playlistId, songId);
      return { success: true };
    }
  },
  Playlist: {
    userId: (parent) => parent.user_id,
  },
};

const server = new ApolloServer({ typeDefs, resolvers });

server.listen({ port: 3002 }).then(({ url }) => {
  console.log(`Node GraphQL API ready at ${url}`);
});
