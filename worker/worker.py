import time
from datetime import datetime
from pymongo import MongoClient


# Connect to MongoDB
client = MongoClient("mongodb://mongodb:27017")
db = client["mydatabase"]
collection = db["jobs"]


def fetch_and_print_objects():
    start_time = time.time()

    objects = collection.find()

    print(f"There is {len(objects)} jobs in mongo")

    end_time = time.time()
    execution_time = end_time - start_time
    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )  # Get the current datetime

    print(f"Current Time: {current_time}")
    print(f"Execution time of fetch_and_print_objects: {execution_time:.5f} seconds")

    time.sleep(2)


while True:
    fetch_and_print_objects()
