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
`;

const resolvers = {
  Query: {
    getUsers: () => db.getUsers(),
    getSongs: () => db.getSongs(),
    getUserPlaylists: (_, { userId }) => db.getUserPlaylists(userId),
    getPlaylistSongs: (_, { playlistId }) => db.getPlaylistSongs(playlistId),
    getSongPlaylists: (_, { songId }) => db.getSongPlaylists(songId),
  },
  Playlist: {
    userId: (parent) => parent.user_id,
  },
};

const server = new ApolloServer({ typeDefs, resolvers });

server.listen({ port: 3002 }).then(({ url }) => {
  console.log(`Node GraphQL API ready at ${url}`);
});
