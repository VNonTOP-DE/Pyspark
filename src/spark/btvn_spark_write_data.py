import json
from pyspark.sql import DataFrame, SparkSession
from typing import Dict
from databases.mongodb_connect import MongoDBConnect
from databases.mysql_connect import MySQLConnect
from pymongo import MongoClient

class SparkWriteDatabases:
    def __init__(self, spark: SparkSession, db_config: Dict):
        self.spark = spark
        self.db_config = db_config

    def spark_write_mysql(self, df_write: DataFrame, table_name: str, jdbc_url: str, config: Dict, mode: str = "append"):
        # Add column spark_temp using MySQL cursor
        try:
            with MySQLConnect(config["host"], config["port"], config["user"], config["password"]) as mysql_client:
                connection, cursor = mysql_client.connection, mysql_client.cursor
                database = "github_data"
                connection.database = database
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN spark_temp VARCHAR(255)")
                connection.commit()
                print("-----------------ADDED Column spark_temp to MySQL------------------")
                mysql_client.close()
        except Exception as e:
            raise Exception(f"-------Failed to connect to MySQL: {e}--------")

        # Spark write DataFrame to MySQL
        df_write.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", table_name) \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .option("driver", config["driver"]) \
            .mode(mode) \
            .save()
        print(f"------Spark wrote data to MySQL table: {table_name} SUCCESSFULLY -----")

    def validate_spark_mysql(self, df_write: DataFrame, table_name: str, jdbc_url: str, config: Dict, mode: str = "append"):
        # Read filtered data from MySQL
        df_read = self.spark.read \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", f"(SELECT * FROM {table_name} WHERE spark_temp = 'sparkwrite') AS subquery") \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .option("driver", config["driver"]) \
            .load()

        # Define subtract_dataframe function
        def subtract_dataframe(df_spark_write: DataFrame, df_read_database: DataFrame):
            result = df_spark_write.exceptAll(df_read_database)
            if not result.isEmpty():
                result.write \
                    .format("jdbc") \
                    .option("url", jdbc_url) \
                    .option("dbtable", table_name) \
                    .option("user", config["user"]) \
                    .option("password", config["password"]) \
                    .option("driver", config["driver"]) \
                    .mode(mode) \
                    .save()
                print(f"-----Spark wrote MISSING RECORDS to MySQL table: {table_name} SUCCESSFULLY ------")

        # Check number of records
        if df_write.count() == df_read.count():
            print(f"--------Validated {df_write.count()} records SUCCESS in total: {df_read.count()} records in MySQL---------")
            subtract_dataframe(df_write, df_read)
        else:
            result = df_write.exceptAll(df_read)
            print(f"---------Missing: {result.count()} Records while Pyspark insert to MySQL---------------")
            result.show()
            subtract_dataframe(df_write, df_read)

        # Drop column spark_temp
        try:
            with MySQLConnect(config["host"], config["port"], config["user"], config["password"]) as mysql_client:
                connection, cursor = mysql_client.connection, mysql_client.cursor
                database = "github_data"
                connection.database = database
                cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN spark_temp")
                connection.commit()
                print("-----------------DROPPED Column spark_temp in MySQL------------------")
                mysql_client.close()
        except Exception as e:
            raise Exception(f"-------Failed to connect to MySQL: {e}--------")

        print("-------Validated Spark Write Data to MySQL SUCCESSFULLY!!!! -----------")

    def spark_write_mongodb(self, df_write: DataFrame, config: Dict, uri: str, database: str, collection: str, mode: str = "append"):
        # Add field spark_temp using MongoDB client
        try:
            with MongoDBConnect(uri, database) as mongo_client:
                # Select the database
                db = mongo_client.db
                # Add new field spark_temp to all documents in the collection
                result = db[collection].update_many(
                    {},  # Empty filter to match all documents
                    {"$set": {"spark_temp": "sparkwrite"}}  # Add spark_temp field
                )
                print(
                    f"-----------------ADDED Field spark_temp to MongoDB collection {database}.{collection} ({result.modified_count} documents updated)------------------")
        except Exception as e:
            raise Exception(f"-------Failed to connect to MongoDB: {str(e)}--------")

        # Write DataFrame to MongoDB
        df_write.write \
            .format("mongo") \
            .option("uri", uri) \
            .option("database", database) \
            .option("collection", collection) \
            .mode(mode) \
            .save()
        print(f"-----Spark wrote data to MongoDB collection: {database}.{collection} SUCCESSFULLY---")

    def subtract_dataframe(self, df_spark_write: DataFrame, df_read_database: DataFrame, uri: str, database: str, collection: str, mode: str = "append"):
        # Subtract df_spark_write vs df_read_database
        result = df_spark_write.exceptAll(df_read_database)
        if not result.isEmpty():
            result.write \
                .format("mongo") \
                .option("uri", uri) \
                .option("database", database) \
                .option("collection", collection) \
                .mode(mode) \
                .save()
            print(f"-----Spark wrote MISSING RECORDS to MongoDB collection {database}.{collection} SUCCESSFULLY ------")
        return result

    def validate_spark_mongodb(self, df_write: DataFrame, config: Dict, uri: str, database: str, collection: str, mode: str = "append") -> DataFrame:
        try:
            # Define the MongoDB aggregation pipeline to filter documents
            # pipeline = [
            #     {"$match": {"spark_temp": "sparkwrite"}}
            # ]

            # Read from MongoDB with the pipeline filter
            df_read = self.spark.read \
                .format("mongo") \
                .option("uri", uri) \
                .option("database", database) \
                .option("collection", collection) \
                .option("pipeline", json.dumps([{"$match": {"spark_temp": "sparkwrite"}}])) \
                .load()
            # Select only the columns matching df_write
            df_read = df_read.select("user_id", "login", "gravatar_id", "url", "avatar_url", "spark_temp")

            print(f"-------------Read filtered DataFrame from MongoDB collection {database}.{collection}---------")

            # Check number of records
            if df_write.count() == df_read.count():
                print(f"--------Validated {df_write.count()} records SUCCESS in total: {df_read.count()} records in MongoDB---------")
                self.subtract_dataframe(df_write, df_read, uri, database, collection, mode)
            else:
                result = df_write.exceptAll(df_read)
                print(f"---------Missing: {result.count()} Records while Pyspark insert to MongoDB---------------")
                result.show()
                self.subtract_dataframe(df_write, df_read, uri, database, collection, mode)

            # Drop field spark_temp from MongoDB collection
            with MongoDBConnect(uri, database) as mongo_client:
                db = mongo_client.db
                result = db[collection].update_many(
                    {},  # Empty filter to match all documents
                    {"$unset": {"spark_temp": ""}}  # Remove spark_temp field
                )
                print(
                    f"-----------------DROPPED Field spark_temp in MongoDB collection {database}.{collection} ({result.modified_count} documents updated)------------------")

            print("-------Validated Spark Write Data to MongoDB SUCCESSFULLY!!!! -----------")
            return df_read

        except Exception as e:
            raise Exception(f"-------Failed to read from or write to MongoDB: {str(e)}--------")

    def write_all_databases(self, df_write: DataFrame, mode: str = "append"):
        self.spark_write_mysql(
            df_write,
            self.db_config["mysql"]["table"],
            self.db_config["mysql"]["jdbc_url"],
            self.db_config["mysql"]["config"],
            mode
        )
        self.spark_write_mongodb(
            df_write,
            self.db_config,
            self.db_config["mongodb"]["uri"],
            self.db_config["mongodb"]["database"],
            self.db_config["mongodb"]["collection"],
            mode
        )
        print("-----------Spark wrote to all databases (MySQL, MongoDB) SUCCESSFULLY!!!!!!!!!-----------")