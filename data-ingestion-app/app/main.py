from pymongo import MongoClient
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType, MapType, TimestampType, LongType
import json
import os
import sys
import logging
from datetime import datetime
from pyspark.sql.functions import current_timestamp
from transformers import DistilBertTokenizer
from transformers import DistilBertModel
import torch
import torch.nn as nn
import numpy as np

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


# Initialize Spark session with Kafka and MongoDB packages
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.mongodb.output.uri", MONGO_URI) \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Define schema for incoming data
schema = StructType([
    StructField("user", StringType(), True),
    StructField("repo", StringType(), True),
    StructField("mainLanguage", StringType(), True),
    StructField("languages", MapType(StringType(), StringType()), True),
    StructField("readme", StringType(), True),
])


# Read data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER_URI) \
    .option("subscribe", "new-git-repository") \
    .load()


# Deserialize JSON data
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")


# ============ FUNCTIONS =================

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
bert_model = DistilBertModel.from_pretrained("distilbert-base-uncased")


def replace_dots_in_keys(languages):
  return {k.replace('.', '_'): v for k, v in languages.items()}


def readme_encode(texts):
    if not texts:
        return []  # Return an empty list if no text is provided

    inputs = tokenizer(texts, padding='max_length', truncation=True, max_length=512, return_tensors="pt")
    with torch.no_grad():
        outputs = bert_model(**inputs)
    
    # Extract the [CLS] token representation and convert it to a list
    sentence_embedding = outputs.last_hidden_state[:, 0, :].squeeze().tolist()
    
    return sentence_embedding


def readme_tokenize(readme):
    tokens = tokenizer.tokenize(readme)
    return " ".join(tokens)


readme_encode_udf = udf(readme_encode, StringType())
replace_dots_udf = udf(replace_dots_in_keys, MapType(StringType(), LongType()))

df = df.withColumn("languages", replace_dots_udf(col("languages")))
df = df.withColumn("processed_readme", readme_encode_udf(col("readme")))
df = df.withColumn("last_updated", current_timestamp())

# ========================================


# Process and write data to MongoDB
def write_to_mongo(df, _):
    df.write \
        .format("mongo") \
        .mode("append") \
        .option("database", "dev") \
        .option("collection", "raw_data") \
        .save()


# Start the streaming query
query = df.writeStream \
    .foreachBatch(write_to_mongo) \
    .start()

query.awaitTermination()