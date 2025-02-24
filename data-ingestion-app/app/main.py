from pymongo import MongoClient
from kafka import KafkaConsumer
import json
import os
import sys

MONGO_URI = os.getenv("MONGO_DB_URI", "mongodb://localhost:27017/")
KAFKA_BROKER_URI = os.getenv("KAFKA_BROKER_URI", "localhost:9094")

try:
  # Establish connection
  client = MongoClient("local")

  # Test the connection
  db_list = client.list_database_names()
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


# Consume messages
for message in consumer:
  if message is not None:
    repo_obj = message.value

    user = repo_obj["user"]
    repo = repo_obj["repo"]

    database = client.get_database("dev")
    collection = database.get_collection("raw_data")


    # TODO prepare data for insertion here


    # Insert or update
    if collection.find_one({"user": user, "repo": repo}):
      print(f"{user}/{repo} already exists in the database. Updating...")
      collection.update_one({"user": user, "repo": repo}, {"$set": repo_obj})
    else:
      collection.insert_one(repo_obj)
      print(f"Inserted new record for {user}/{repo}.")
  else:
    print("No message received")
