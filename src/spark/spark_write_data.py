from pyspark.sql import SparkSession, DataFrame
from typing import Dict

from databases.mysql_connect import MySQLConnect


class SparkWriteDatabases:
    def __init__(self, spark : SparkSession, db_config: Dict ):
        self.spark = spark
        self.db_config = db_config



        #muc dich: write data vao mysql
        #can truyen vao cac tham so j?
    #step
    #database: khoi tao spark -> create dataframe -> set up config -> use spark write data to mysql
    def spark_write_mysql(self, df_write: DataFrame, table_name: str, jdbc_url: str, config: Dict, mode: str = "append"):

        #Add column Spark_temp using python cursor in mySQL
        try:
            with MySQLConnect(config["host"], config["port"], config["user"],
                              config["password"]) as mysql_client:
                connection, cursor = mysql_client.connection, mysql_client.cursor
                database = "github_data"
                connection.database = database
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN spark_temp VARCHAR(255)")
                connection.commit()
                print("-----------------ADDED Column Spark_temp to mySQL------------------")
                mysql_client.close()
        except Exception as e:
            raise Exception(f"-------Failed to connect mysql: {e}--------")

        #Spark write dataframe to MySQL
        df_write.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", table_name) \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .option("driver", config["driver"]) \
            .mode(mode) \
            .save()

        print(f"------spark wrote data to mysql table : {table_name} SUCCESSFULLY -----")


    def validate_spark_mysql(self,df_write: DataFrame, table_name: str, jdbc_url: str, config: Dict, mode :str = "append"):
        df_read = self.spark.read \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", f"(SELECT * FROM {table_name} WHERE spark_temp = 'sparkwrite') AS subquery") \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .option("driver", config["driver"]) \
            .load()

        # df_read.show()



        def subtract_dataframe(df_spark_write: DataFrame, df_read_database: DataFrame):
            #subtract df_write vs df_read
            result = df_spark_write.exceptAll(df_read_database)
            # print(f"---WARNING:::--------RECORDS MISSING : {result.count()}------------")
            # result.show()
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

                print(f"-----spark wrote MISSING RECORDS to mysql table : {table_name} SUCCESSFULLY ------")


         # check Number of records
        if df_write.count() == df_read.count():
            print(f"--------validate {df_write.count()} records SUCCESS in total: {df_read.count()} records in MYSQL---------")
            subtract_dataframe(df_write, df_read)
        else:
            print(f"---------Missing: {result.count()} Records while Pyspark insert to MYSQL---------------")
            result.show()
            subtract_dataframe(df_write, df_read)

        #drop column spark_temp
        try:
            with MySQLConnect(config["host"], config["port"], config["user"],
                              config["password"]) as mysql_client:
                connection, cursor = mysql_client.connection, mysql_client.cursor
                database = "github_data"
                connection.database = database
                cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN spark_temp")
                connection.commit()
                print("-----------------DROPPED Column Spark_temp in mySQL------------------")
                mysql_client.close()
        except Exception as e:
            raise Exception(f"-------Failed to connect mysql: {e}--------")

        print("-------Validate Spark Write Data to MYSQL SUCCESSFULLY!!!! -----------")


    def spark_write_mongodb(self, df_write : DataFrame, uri: str, database: str, collection: str, mode : str = "append" ):
        df_write.write \
            .format("mongo") \
            .option("uri", uri) \
            .option("database", database) \
            .option("collection", collection) \
            .mode(mode) \
            .save()
        print(f"-----spark write data to mongodb collection: {collection} SUCCESSFULLY---")


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