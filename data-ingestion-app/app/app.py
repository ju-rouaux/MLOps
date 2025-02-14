from pymongo import MongoClient
from kafka import KafkaConsumer
import json
import os

MONGO_URI = os.getenv("MONGO_DB_URI", "mongodb://localhost:27017/")
KAFKA_BROKER_URI = os.getenv("KAFKA_BROKER_URI", "localhost:9094")

try:
    # Establish connection
    client = MongoClient(MONGO_URI)

    # Test the connection
    db_list = client.list_database_names()
    print("Connected to MongoDB successfully!")
    print("Databases:", db_list)

    # Optionally, check a specific database
    db_name = "test"  # Change this to your database name
    if db_name in db_list:
        print(f"Database '{db_name}' exists.")
    else:
        print(f"Database '{db_name}' not found. It will be created upon first document insertion.")


    # Initialize the consumer
    consumer = KafkaConsumer(
      'foobar',
      bootstrap_servers=KAFKA_BROKER_URI,
      enable_auto_commit=True,

      
      value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    print("connected")

    # Consume messages
    for message in consumer:
      if message is not None:
        print(f"Received message: {message.value}")
        database = client.get_database("dev")
        collection = database.get_collection("test")
        collection.insert_one(message.value)
      else:
        print("No message received")

except Exception as e:
    print("Error connecting to MongoDB:", e)
finally:
    client.close()


