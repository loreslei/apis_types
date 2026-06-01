import grpc
import time
from locust import User, task, between
import sys
import os

# Import compiled protobuf files
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python_services', 'grpc'))
import music_pb2
import music_pb2_grpc

class GrpcClient:
    def __init__(self, environment, host):
        self.env = environment
        self.channel = grpc.insecure_channel(host)
        self.stub = music_pb2_grpc.MusicServiceStub(self.channel)

    def get_users(self):
        start_time = time.time()
        try:
            res = self.stub.GetUsers(music_pb2.Empty())
            total_time = int((time.time() - start_time) * 1000)
            self.env.events.request.fire(
                request_type="grpc", name="GetUsers", response_time=total_time, response_length=0
            )
            return res
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            self.env.events.request.fire(
                request_type="grpc", name="GetUsers", response_time=total_time, exception=e, response_length=0
            )

    def get_user_playlists(self):
        start_time = time.time()
        try:
            res = self.stub.GetUserPlaylists(music_pb2.IdRequest(id=1))
            total_time = int((time.time() - start_time) * 1000)
            self.env.events.request.fire(
                request_type="grpc", name="GetUserPlaylists", response_time=total_time, response_length=0
            )
            return res
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            self.env.events.request.fire(
                request_type="grpc", name="GetUserPlaylists", response_time=total_time, exception=e, response_length=0
            )


class GrpcUser(User):
    wait_time = between(0.1, 0.5)
    
    def __init__(self, environment):
        super().__init__(environment)
        # Using self.host since we'll pass --host
        host = self.host.replace("http://", "").replace("https://", "") if self.host else "127.0.0.1:3003"
        self.client = GrpcClient(environment, host)

    @task
    def get_users(self):
        self.client.get_users()

    @task
    def get_user_playlists(self):
        self.client.get_user_playlists()
