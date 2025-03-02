from pymongo import MongoClient
from kafka import KafkaConsumer
import json
import os
import sys
import logging
from datetime import datetime


MONGO_URI = os.getenv("MONGO_DB_URI", "mongodb://localhost:27017/")
KAFKA_BROKER_URI = os.getenv("KAFKA_BROKER_URI", "localhost:9094")

try:
  # Establish connection
  client = MongoClient(MONGO_URI)

  # Test the connection
  db_list = client.list_database_names()
  db = client.get_database("dev")
  collection = db.get_collection("raw_data")
  print("Successfully connected to MongoDB")
  print("Databases:", db_list)

except Exception as e:
  print("Error connecting to MongoDB:", e)
  sys.exit(1)  # Exit the program if connection fails


# Initialize the consumer
consumer = KafkaConsumer(
  'new-git-repository',
  bootstrap_servers=KAFKA_BROKER_URI,
  enable_auto_commit=True,
  value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
print("Successfully connected to Kafka")



# Function to validate and clean data
def validate_and_prepare_data(repo_obj):
    required_fields = ["user", "repo", "languages", "readme"]
    for field in required_fields:
        if field not in repo_obj:
            logging.warning(f"Missing field {field} in received data: {repo_obj}")
            return None
    
    repo_obj["last_updated"] = datetime.now()
    return repo_obj


# Consume messages
print("Listening for messages...")

for message in consumer:
    try:
        if message is not None:
            repo_obj = message.value
            processed_data = validate_and_prepare_data(repo_obj)
            
            if processed_data:
                filter_query = {"user": processed_data["user"], "repo": processed_data["repo"]}
                update_data = {"$set": processed_data}
                collection.update_one(filter_query, update_data, upsert=True)
                logging.info(f"Inserted/Updated repository: {processed_data['user']}/{processed_data['repo']}")
            else:
                logging.warning("Invalid data received, skipping insertion.")
    except Exception as e:
        logging.error(f"Error processing message: {e}")



