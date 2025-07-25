from pyspark.sql.functions import *
from pyspark.sql.types import *

from pyspark.sql import SparkSession

def main():
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("ShopeeProductProcessing") \
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.3,org.mongodb.spark:mongo-spark-connector_2.12:10.5.0") \
        .getOrCreate()

    # Define schema for the incoming Kafka data
    schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("login", StringType(), True),
        StructField("gravatar_id", StringType(), True),
        StructField("avatar_url", StringType(), True),
        StructField("url", StringType(), True),
        StructField("status", StringType(), True),  # Changed 'state' to 'status' to match producer schema
        StructField("log_timestamp", StringType(), True),
        StructField("message_id", StringType(), True),  # Added for validation
        StructField("hash", StringType(), True)  # Added for validation
    ])

    # Read from the spark_input Kafka topic
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "192.168.2.26:9092") \
        .option("subscribe", "spark_input") \
        .option("startingOffsets", "earliest") \
        .load()

    # Parse JSON from Kafka message value
    df_property = kafka_df.select(col("value").cast("string")) \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Write stream to console for debugging
    console_query = df_property.writeStream \
        .format("console") \
        .queryName("ConsoleOutput") \
        .option("forceDeleteTempCheckpointLocation", "true") \
        .outputMode("append") \
        .start()

    # Optional: Write to MongoDB (uncomment to enable)
    # mongo_stream = df_property.writeStream \
    #     .format("mongodb") \
    #     .option("checkpointLocation", "/home/prime/PycharmProjects/DE-ETL-102/checkpoint/pyspark") \
    #     .option("forceDeleteTempCheckpointLocation", "true") \
    #     .option('spark.mongodb.connection.uri', 'mongodb://datdepzai:datdepzaivailon@localhost:27017') \
    #     .option('spark.mongodb.database', 'github_data') \
    #     .option('spark.mongodb.collection', 'users') \
    #     .trigger(continuous="0.1 seconds") \
    #     .outputMode("append") \
    #     .start()

    console_query.awaitTermination()
    # mongo_stream.awaitTermination()  # Uncomment if using MongoDB sink

if __name__ == "__main__":
    main()