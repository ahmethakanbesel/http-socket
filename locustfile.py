from locust import HttpUser, task


class ExampleServer(HttpUser):
    @task
    def index(self):
        self.client.get("http://localhost:8000/index")
