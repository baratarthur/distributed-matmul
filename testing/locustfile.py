from locust import HttpUser, task, constant
from datetime import datetime
import csv
import random

random.seed(42)

class StressTestUser(HttpUser):
    wait_time = constant(1)

    @task
    def stress_test(self):
        size = 20
        lines_A = ",".join([f"[{','.join(map(str, [random.randint(0, 10) for _ in range(size)]))}]" for _ in range(size)])
        lines_I = ",".join([f"[{','.join(['1' if i == j else '0' for i in range(size)])}]" for j in range(size)])
        A = f"[{lines_A}]"
        I = f"[{lines_I}]"

        now = datetime.now()

        with self.client.post("/matmul",
                              json={"A": A, "B": I},
                              catch_response=True) as response:
            # Log to CSV
            with open('results/dana_requests.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([now, response.request_meta["response_time"], response.status_code])

            if response.text == A:
                response.success()
            else:
                response.failure("Wrong response")