from locust import HttpUser, task, between

class RestUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def get_users(self):
        self.client.get("/users", name="/users")

    @task
    def get_user_playlists(self):
        self.client.get("/users/1/playlists", name="/users/[id]/playlists")
