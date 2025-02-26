from locust import HttpUser, task, between
import random

class OrderLoadTest(HttpUser):
    wait_time = between(1, 3)
    created_orders = []  # ✅ Stores created order IDs

    @task
    def create_order(self):
        item_count = random.randint(1, 25)  # ✅ Choose random size between 1 and 25
        response = self.client.post("/orders", json={
            "user_id": random.randint(1, 100),
            "item_ids": [random.randint(1, 1000) for _ in range(item_count)],  # ✅ Dynamic size
            "total_amount": round(random.uniform(10, 500), 2)
        })
        
        if response.status_code == 201:
            order_id = response.json().get("order_id")  # ✅ Ensure correct key
            if order_id:
                self.created_orders.append(order_id)  # ✅ Store created order ID

    @task
    def check_order_status(self):
        if self.created_orders:
            order_id = random.choice(self.created_orders)  # ✅ Pick a random order
            self.client.get(f"/orders/{order_id}")

    @task
    def get_metrics(self):
        self.client.get("/metrics")


