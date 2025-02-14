from kafka import KafkaProducer
import time
import random
import os

# Initialize the producer
KAFKA_BROKER_URI = os.getenv("KAFKA_BROKER_URI", "localhost:9094")
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URI)

while True:
    time.sleep(5)
    print("Sending...")
    random_value = random.random()
    producer.send('foobar', f"""
    {{
      "test_value": {random_value}
    }}
    """.encode('utf-8'))