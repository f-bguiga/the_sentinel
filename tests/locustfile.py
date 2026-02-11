from locust import HttpUser, task, between

class FraudAPIUser(HttpUser):
    wait_time = between(1, 2) # Simulate users waiting 1-2s between clicks

    @task
    def predict_fraud(self):
        self.client.post("/predict", json={"id": 1, "amount": 500.0})

    @task(3) # This task runs 3x more often
    def health_check(self):
        self.client.get("/")