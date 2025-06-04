from pyspark.sql import SparkSession, DataFrame
from typing import Dict


class SparkWriteDatabases:
    def __init__(self, spark : SparkSession, db_config: Dict ):
        self.spark = spark
        self.db_config = db_config



        #muc dich: write data vao mysql
        #can truyen vao cac tham so j?
    #step
    #database: khoi tao spark -> create dataframe -> set up config -> use spark write data to mysql
    def spark_write_mysql(self, df: DataFrame, table_name: str, jdbc_url: str, config: Dict, mode: str = "append"):


        df.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", table_name) \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .option("driver", config["driver"]) \
            .mode(mode) \
            .save()

        print(f"------spark wrote data to mysql table : {table_name} SUCCESSFULLY -----")

