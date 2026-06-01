from locust import HttpUser, task, between

class SOAPUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def get_users(self):
        if self.host.endswith("3004"):
            body = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/music">
              <soap:Body>
                <tns:GetUsersRequest></tns:GetUsersRequest>
              </soap:Body>
            </soap:Envelope>"""
            self.client.post("/music", data=body, headers={"Content-Type": "text/xml"}, name="GetUsers")
        else:
            body = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/music">
              <soap:Body>
                <tns:GetUsers></tns:GetUsers>
              </soap:Body>
            </soap:Envelope>"""
            self.client.post("/", data=body, headers={"Content-Type": "text/xml"}, name="GetUsers")

    @task
    def get_user_playlists(self):
        if self.host.endswith("3004"):
            body = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/music">
              <soap:Body>
                <tns:IdRequest>
                  <tns:id>1</tns:id>
                </tns:IdRequest>
              </soap:Body>
            </soap:Envelope>"""
            self.client.post("/music", data=body, headers={"Content-Type": "text/xml"}, name="GetUserPlaylists")
        else:
            body = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/music">
              <soap:Body>
                <tns:GetUserPlaylists>
                  <tns:id>1</tns:id>
                </tns:GetUserPlaylists>
              </soap:Body>
            </soap:Envelope>"""
            self.client.post("/", data=body, headers={"Content-Type": "text/xml"}, name="GetUserPlaylists")
