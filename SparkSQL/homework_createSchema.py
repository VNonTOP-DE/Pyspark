from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession.builder.appName("vnontop").master("local[*]") \
    .config("spark.executor.memory", "4gb").getOrCreate()

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

df = spark.read.schema(schema_json).json("C:\\Users\\Public\\PYSPARK_Python_Learn\\StudyData\\2015-03-01-17.json")

#print(df.count())
#df.show(5, truncate=False)