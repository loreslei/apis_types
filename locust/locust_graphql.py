from locust import HttpUser, task, between

class GraphQLUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def get_users(self):
        query = """
        query {
            getUsers {
                id
                name
                age
            }
        }
        """
        self.client.post("/graphql" if self.host.endswith("8002") else "/", json={'query': query}, name="getUsers")

    @task
    def get_user_playlists(self):
        query = """
        query {
            getUserPlaylists(userId: 1) {
                id
                name
                userId
            }
        }
        """
        self.client.post("/graphql" if self.host.endswith("8002") else "/", json={'query': query}, name="getUserPlaylists")
