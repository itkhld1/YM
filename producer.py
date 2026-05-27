import requests
import random
import uuid
import time
from datetime import datetime

# 1. THE DOMAIN OBJECT
class LogEntry:
    def __init__(self):
        # Fields based on your whiteboard notes
        self.user_id = None
        self.token = None
        self.email = None
        self.credit_card = None
        self.password = None
        self.transaction_time = None
        self.level = None

    # This makes the log look nice when we print it
    def to_dict(self):
        return self.__dict__


# 2. THE BUILDER PATTERN (Design Pattern #1)
class LogBuilder:
    def __init__(self):
        self.log = LogEntry()

    def set_base_info(self):
        self.log.user_id = random.randint(1000, 9999)
        self.log.transaction_time = datetime.now().isoformat()
        # Adding different levels so we can test the "Filtre" and "Performans" stage later
        self.log.level = random.choice(["INFO", "WARNING", "ERROR", "DEBUG"])
        return self

    def set_security_info(self):
        self.log.token = str(uuid.uuid4())
        self.log.password = f"secret_{random.randint(1000, 9999)}"
        return self

    def set_personal_info(self):
        self.log.email = f"user{self.log.user_id}@example.com"
        # Simulate realistic data: Not every log might have a credit card
        if random.choice([True, False]):
            self.log.credit_card = f"{random.randint(4000, 4999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        self.log.message = f"User {self.log.user_id} performed an action with status {self.log.level}"
        return self

    def build(self):
        return self.log



# 3. THE GENERATOR FUNCTION
def generate_logs(count=5):
    logs = []
    for _ in range(count):
        # Using the Builder to construct the log step by step
        builder = LogBuilder()
        log = builder.set_base_info().set_security_info().set_personal_info().build()
        logs.append(log.to_dict())
    return logs


# TEST RUN
if __name__ == "__main__":
    LOG_COUNT = 1000
    print(f"Firing {LOG_COUNT} dummy logs to the Consumer...\n")
    dummy_data = generate_logs(LOG_COUNT)

    start_time = time.time()
    success_count = 0
    
    for item in dummy_data:
        try:
            # Send the JSON log to Flask Consumer
            response = requests.post("http://consumer:5001/ingest", json=item)
            if response.status_code == 200:
                success_count += 1
        except Exception as e:
            print(f"Failed to send: {e}")

    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "="*40)
    print("PERFORMANCE REPORT")
    print(f"Total Logs Sent: {LOG_COUNT}")
    print(f"Successful Ingestions: {success_count}")
    print(f"Total Time Taken: {total_time:.2f} seconds")
    print(f"Throughput: {LOG_COUNT / total_time:.2f} logs/second")
    print("="*40)