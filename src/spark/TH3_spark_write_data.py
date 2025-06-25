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
    def spark_write_table(self, df_write: DataFrame,  mode: str = "overwrite"):


        #Spark write dataframe to new table
        df_write \
            .write \
            .mode(mode) \
            .saveAsTable("spark_table_temp")

        print(f"------spark wrote data to table spark_table_temp SUCCESSFULLY -----")

    def subtract_dataframe(self, df_spark_write: DataFrame, df_read_table: DataFrame,
                           table_name: str = "spark_table_temp", mode: str = "append"):
        result = df_spark_write.exceptAll(df_read_table)
        missing_count = result.count()

        if missing_count > 0:
            print(f"---WARNING: {missing_count} records missing in {table_name}---")
            result.show(10, truncate=False)
            # Write missing records back to spark_table_temp
            result.write.mode(mode).saveAsTable(table_name)
            print(f"-----Spark wrote {missing_count} MISSING RECORDS to table: {table_name} SUCCESSFULLY------")
        else:
            print(f"-----No missing records found in {table_name}-----")


    def validate_spark(self,df_write: DataFrame, mode :str = "append" ):
        df_read = self.spark.table("spark_table_temp")
        # df_read.show()
        # check Number of records
        # Step 2: Validate record count
        original_count = df_write.count()
        read_count = df_read.count()
        print(f"Total records in original DataFrame: {original_count}")
        print(f"Total records in spark_table_temp: {read_count}")

        if original_count == read_count:
            print(f"--------Validated {read_count} records SUCCESSFULLY---------")
        else:
            print(
                f"---------Record count mismatch: {original_count} (original) vs {read_count} (spark_table_temp)---------------")




        #  Deduplicate spark_table_temp by 'id' (keep first occurrence)
        df_read_dedup = df_read.dropDuplicates(["id"])
        print(f"Number of records after deduplication: {df_read_dedup.count()}")

        return df_read_dedup
        #OPTION 2: USE LEFT ANTI JOIN
    #     # Step 6: Find records in spark_table_temp not in MySQL users
    #     missing_records = df_read_dedup.join(df_mysql, "id", "left_anti")
    #     missing_count = missing_records.count()
    #     print(f"Number of records in spark_table_temp not in MySQL users: {missing_count}")
    #
    #     if missing_count > 0:
    #         print("Missing records found. Writing to MySQL users table...")
    #         try:
    #             missing_records.write \
    #             .format("jdbc") \
    #             .option("url", jdbc_url) \
    #             .option("dbtable", table_name) \
    #             .option("user", config["user"]) \
    #             .option("password", config["password"]) \
    #             .option("driver", config["driver"]) \
    #             .mode(mode) \
    #             .save()
    #             print(f"-----Successfully wrote {missing_count} missing records to MySQL users table-----")
    #         except Exception as e:
    #             print(f"Error writing to MySQL users table: {str(e)}")
    #             raise
    #     else:
    #         print("No missing records found. No data written to MySQL.")
    #
    # except Exception as e:
    # print(f"Error during validation: {str(e)}")
    # raise

    def read_spark_mysql(self, table_name: str, jdbc_url: str, config: Dict):
        df_mysql = self.spark.read \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", table_name) \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .option("driver", config["driver"]) \
            .load()
        return df_mysql


    def filter_record(self, df_mysql: DataFrame, df_read_dedup: DataFrame):
        #  Use unionAll and distinct to combine and get unique records
        # Ensure both DataFrames have the same columns for unionAll
        df_mysql_selected = df_mysql.select(df_read_dedup.columns)
        combined_df = df_read_dedup.unionAll(df_mysql_selected)
        unique_df = combined_df.dropDuplicates(["id"])
        print(f"Number of unique records after unionAll and distinct: {unique_df.count()}")
        return unique_df
        #  Overwrite MySQL users table with unique records

    print("Overwriting MySQL users table with unique records...")

    def spark_write_mysql(self, unique_df: DataFrame, table_name: str, jdbc_url: str, config: Dict, mode: str = "append"):

        #Spark write dataframe to MySQL
        unique_df.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", table_name) \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .option("driver", config["driver"]) \
            .mode(mode) \
            .save()

        print(f"------spark wrote new data to mysql table : {table_name} SUCCESSFULLY -----")



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