from pyspark.sql.functions import col

from config.spark_config import SparkConnect
from pyspark.sql.types import *
from config.database_config import get_spark_config
from src.spark.spark_write_data import SparkWriteDatabases
def main():
    jars = [
        "mysql:mysql-connector-java:8.0.33"
    ]
    sparkconnect = SparkConnect(
        app_name="vnontop",
        master_url="local[*]",
        executor_cores=1,
        driver_memory="2g",
        num_executors=1,
        jar_packages= jars,
        log_level="DEBUG"
    )
    schema_json = StructType([
        StructField("id", LongType(), False),
        StructField("type", StringType(), True),
        StructField("actor", StructType([
            StructField("id", LongType(), False),
            StructField("login", StringType(), True),
            StructField("gravatar_id", StringType(), True),
            StructField("url", StringType(), True),
            StructField("avatar_url", StringType(), True)
        ]), True),
        StructField("repo", StructType([
            StructField("id", LongType(), False),
            StructField("name", StringType(), True),
            StructField("url", StringType(), True)
        ]), True),
        StructField("public", BooleanType(), True),
        StructField("created_at", TimestampType(), True),
        StructField("org", StructType([
            StructField("id", LongType(), False),
            StructField("gravatar_id", StringType(), True),
            StructField("url", StringType(), True),
            StructField("avatar_url", StringType(), True)
        ]), True)
    ])
    df = sparkconnect.spark.read.schema(schema_json).json("C:\\Users\\Public\\PythonProject1\\data\\2015-03-01-17.json")

    df_write_table = df.select(
        col("actor.id").alias("users_id"),
        col("actor.login").alias("login"),
        col("actor.gravatar_id").alias("gravatar_id"),
        col("actor.url").alias("url"),
        col("actor.avatar_url").alias("avatar_url")
    )

    spark_configs = get_spark_config()

    df_write = SparkWriteDatabases(sparkconnect.spark, spark_configs)
    df_write.spark_write_mysql(df_write_table, spark_configs["mysql"]["table"], spark_configs["mysql"]["jdbc_url"],
                               spark_configs["mysql"]["config"])


if __name__ == "__main__":
    main()