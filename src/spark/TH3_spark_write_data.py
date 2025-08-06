from pyspark.sql import SparkSession, DataFrame
from typing import Dict

from config.database_config import get_database_config
from databases.mongodb_connect import MongoDBConnect
from databases.mysql_connect import MySQLConnect


class SparkWriteDatabases:
    def __init__(self, spark : SparkSession, db_config: Dict ):
        self.spark = spark
        self.db_config = db_config

    #step
    #database: khoi tao spark -> create dataframe -> set up config -> use spark write data to mysql
    def spark_write_table(self, df_write: DataFrame, jdbc_url : str, config : Dict,  mode: str = "overwrite"):
        df_write.write \
                .format("jdbc") \
                .option("url", jdbc_url) \
                .option("dbtable", "spark_table_temp") \
                .option("user", config["user"]) \
                .option("password", config["password"]) \
                .option("driver", config["driver"]) \
                .mode(mode) \
                .save()

        print(f"------spark wrote new data to mysql table : spark_table_temp SUCCESSFULLY -----")



    def validate_spark_mysql(self,df_write: DataFrame, jdbc_url: str, config:Dict, mode :str = "append", table_name: str = "spark_table_temp" ):
        df_read = self.spark.read \
                .format("jdbc") \
                .option("url", jdbc_url) \
                .option("dbtable", table_name) \
                .option("user", config["user"]) \
                .option("password", config["password"]) \
                .option("driver", config["driver"]) \
                .load()

        def subtract_dataframe(df_spark_write: DataFrame, df_read_table: DataFrame):
            result = df_spark_write.exceptAll(df_read_table)


            if not result.isEmpty():
                result \
                    .write \
                    .format("jdbc") \
                    .option("url", jdbc_url) \
                    .option("dbtable", "spark_table_temp") \
                    .option("user", config["user"]) \
                    .option("password", config["password"]) \
                    .option("driver", config["driver"]) \
                    .mode(mode) \
                    .save()

                print(f"------spark wrote MISSING data to table : spark_table_temp SUCCESSFULLY -----")
            else:
                print(f"-----No missing records found in spark_table_temp-----")
        if df_write.count() != df_read.count():
            print(f"------Missing data in table: {table_name}, writing Missing data to table: {table_name}...------")
            subtract_dataframe(df_write, df_read)
        else:
            print(f"Validated :{df_read.count()} records in spark_table_temp")
            subtract_dataframe(df_write, df_read)
        print(f"--------Validated Spark write data to table : spark_table_temp successfully----------")


    def insert_data_mysql(self, config: Dict):
        with MySQLConnect(config["host"], config["port"], config["user"],
                          config["password"]) as mysql_client:
            connection, cursor = mysql_client.connection, mysql_client.cursor
            database = get_database_config()["mysql"].database
            connection.database = database
            cursor.execute("SELECT s.* from spark_table_temp s LEFT JOIN users u ON u.user_id = s.user_id WHERE u.user_id IS NULL;")
            records = []
            row = cursor.fetchone()

            while row:
                records.append(row)
                row = cursor.fetchone()


            for rec in records:
                try:
                    cursor.execute("INSERT INTO users(user_id, login, gravatar_id, url, avatar_url) VALUES(%s,%s,%s,%s,%s)",
                            rec)
                    connection.commit()
                    print("-----insert data into mysql successfully-----")
                except Exception as e:
                    print(f"Error inserting record {rec}: {str(e)}")
                    continue

    def spark_write_collection(self, df_write: DataFrame, uri: str, database: str,  mode: str = "overwrite"):
        df_write.write \
            .format("mongo") \
            .option("uri", uri) \
            .option("database", database) \
            .option("collection", "spark_table_temp") \
            .mode(mode) \
            .save()
        print(f"-----Spark wrote data to MongoDB collection: {database}.spark_table_temp SUCCESSFULLY---")

    def validate_spark_mongodb(self,df_write: DataFrame, uri:str, database: str, collection: str = "spark_table_temp"):
        # Read from MongoDB
        df_read = self.spark.read \
            .format("mongo") \
            .option("uri", uri) \
            .option("database", database) \
            .option("collection", collection) \
            .load()
        # Select only the columns matching df_write
        df_read = df_read.select("user_id", "login", "gravatar_id", "url", "avatar_url")

        print(f"-------------Read DataFrame from MongoDB collection {database}.{collection}---------")

        def subtract_dataframe(df_spark_write: DataFrame, df_read_collection: DataFrame, mode: str = "append"):
            result = df_spark_write.exceptAll(df_read_collection)


            if not result.isEmpty():
                result \
                    .write \
                    .format("mongo") \
                    .option("uri", uri) \
                    .option("database", database) \
                    .option("collection", "spark_table_temp") \
                    .mode(mode) \
                    .save()

                print(f"------spark wrote MISSING data to collection : spark_table_temp SUCCESSFULLY -----")
            else:
                print(f"-----No missing records found in spark_table_temp-----")
        if df_write.count() != df_read.count():
            print(f"------Missing data in collection: {collection}, writing Missing data to collection: {collection}...------")
            subtract_dataframe(df_write, df_read)
        else:
            print(f"Validated :{df_read.count()} records in spark_table_temp")
            subtract_dataframe(df_write, df_read)
        print(f"--------Validated Spark write data to collection : spark_table_temp successfully----------")

    def insert_data_mongodb(self, uri, database):
        with MongoDBConnect(uri, database) as mongo_client:
            db = mongo_client.db
            try:
                # Define the aggregation pipeline to find spark_table_temp documents
                # where user_id does not exist in the users collection
                pipeline = [
                    {
                        "$lookup": {
                            "from": "users",  # The users collection
                            "localField": "user_id",  # Field in spark_table_temp
                            "foreignField": "user_id",  # Field in users
                            "as": "user_data"  # Temporary array to store joined data
                        }
                    },
                    {
                        "$match": {
                            "user_data": {"$eq": []}  # Filter where no matching users were found
                        }
                    },
                    {
                        "$project": {
                            "user_id": 1,  # Include fields to insert
                            "login": 1,
                            "gravatar_id": 1,
                            "url": 1,
                            "avatar_url": 1,
                            "_id": 0  # Exclude the _id field
                        }
                    }
                ]

                # Execute the aggregation pipeline
                records = list(db["spark_table_temp"].aggregate(pipeline))

                # Insert matching records into the users collection
                if records:
                    for rec in records:
                        try:
                            db["users"].insert_one({
                                "user_id": rec.get("user_id"),
                                "login": rec.get("login"),
                                "gravatar_id": rec.get("gravatar_id"),
                                "url": rec.get("url"),
                                "avatar_url": rec.get("avatar_url")
                            })
                            print(
                                f"-----Inserted document with user_id {rec.get('user_id')} into users collection-----")
                        except Exception as e:
                            print(f"Error inserting record {rec}: {str(e)}")
                            continue
                    print(f"-----Successfully scanned {len(records)} documents into users collection-----")
                else:
                    print("No documents found to insert")

            except Exception as e:
                print(f"Error during MongoDB operation: {str(e)}")
def write_all_databases(self, df_write: DataFrame, mode: str = "append" ):
        self.spark_write_mysql(
            df_write,
            self.db_config["mysql"]["table"],
            self.db_config["mysql"]["jdbc_url"],
            self.db_config["mysql"]["config"],
            mode
        )
        self.spark_write_mongodb(
            df_write,
            self.db_config["mongodb"]["uri"],
            self.db_config["mongodb"]["database"],
            self.db_config["mongodb"]["collection"],
            mode
        )
        print("-----------Spark wrote all database (MYSQL,MONGODB)!!!!!!!!!-----------")