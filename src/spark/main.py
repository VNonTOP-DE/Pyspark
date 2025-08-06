from pyspark.sql.functions import col, lit

from config.spark_config import SparkConnect
from pyspark.sql.types import *
from config.database_config import get_spark_config
from src.spark.TH3_spark_write_data import SparkWriteDatabases
def main():
    jars = [
        "mysql:mysql-connector-java:8.0.33",
        "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1"
    ]
    sparkconnect = SparkConnect(
        app_name="vnontop",
        master_url="local[*]",
        executor_cores=1,
        driver_memory="2g",
        num_executors=1,
        jar_packages= jars,
        log_level="INFO"
    )
    schema_json = StructType([
        StructField('actor', StructType([
            StructField('id', IntegerType(), True),
            StructField('login', StringType(), True),
            StructField('gravatar_id', StringType(), True),
            StructField('url', StringType(), True),
            StructField('avatar_url', StringType(), True),
        ]), True),
        StructField('repo', StructType([
            StructField('id', LongType(), False),
            StructField('name', StringType(), True),
            StructField('url', StringType(), True),
        ]), True)
    ])
    df = sparkconnect.spark.read.schema(schema_json).json("C:\\Users\\Public\\PythonProject1\\data\\2015-03-01-17.json")

    df_write_table = df.withColumn('spark_temp', lit('sparkwrite')).select(
        col("actor.id").alias("user_id"),
        col("actor.login").alias("login"),
        col("actor.gravatar_id").alias("gravatar_id"),
        col("actor.url").alias("url"),
        col("actor.avatar_url").alias("avatar_url"),
        # col("spark_temp").alias("spark_temp")
    )

    spark_configs = get_spark_config()

    df_write = SparkWriteDatabases(sparkconnect.spark, spark_configs)

    # df_write.write_all_databases(df_write_table)
    df_write.spark_write_table(df_write_table,spark_configs["mysql"]["jdbc_url"], spark_configs["mysql"]["config"] )
    df_write.spark_write_collection(df_write_table, spark_configs["mongodb"]["uri"], spark_configs["mongodb"]["database"])
    #validate
    df_write.validate_spark_mysql(df_write_table,spark_configs["mysql"]["jdbc_url"], spark_configs["mysql"]["config"] ,mode="append")
    df_write.validate_spark_mongodb(df_write_table, spark_configs["mongodb"]["uri"], spark_configs["mongodb"]["database"] )
    #df_write.validate_spark_mongodb(df_write_table, spark_configs, spark_configs["mongodb"]["uri"], spark_configs["mongodb"]["database"],spark_configs["mongodb"]["collection"] )

    df_write.insert_data_mysql(spark_configs["mysql"]["config"])
    df_write.insert_data_mongodb(spark_configs["mongodb"]["uri"], spark_configs["mongodb"]["database"])
    # df_write.validate_spark_all_databases(df_write_table, mode="append")

if __name__ == "__main__":
    main()