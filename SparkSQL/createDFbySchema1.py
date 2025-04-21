from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.types import *
from datetime import datetime


spark = SparkSession.builder \
    .appName("vnontop") \
    .config("spark.executor.memory", "4gb") \
    .master("local[*]") \
    .getOrCreate()

data = [
    Row(
        name = "dat",
        age = 30,
        id = 1,
        salary = 50000.0,
        bonus = 2500.75,
        is_active = True,
        scores = [15, 85, 100],
        attributes = {"dept": "engineering", "role": "develop"},
        hire_date = datetime.strptime("2023-01-15", "%Y-%m-%d").date(), #convert a string to date
        last_login = datetime.strptime("2025-04-16 10:30:05", "%Y-%m-%d %H:%M:%S"), #convert string to datetime

    ),
    Row(
        name="vnontop",
        age=80,
        id=2,
        salary=90000.0,
        bonus=500.45,
        is_active=False,
        scores=[89, 85, 100],
        attributes={"dept": "engineering", "role": "software"},
        hire_date=datetime.strptime("2009-04-17", "%Y-%m-%d").date(),  # convert a string to date
        last_login=datetime.strptime("2024-07-25 20:30:05", "%Y-%m-%d %H:%M:%S"),  # convert string to datetime

    )
]

schemapeople = StructType([
    StructField("name", StringType(), True),
    StructField("age", ByteType(), True ),
    StructField("id", IntegerType(), False),
    StructField("salary", DoubleType(), True),
    StructField("bonus", DoubleType(), True),
    StructField("is_active", BooleanType(), True),
    StructField("scores", ArrayType(IntegerType()), True),
    StructField("attributes", MapType(StringType(), StringType()), True),
    StructField("hire_date", DateType(), True),
    StructField("last_login", TimestampType(), True),
])


df= spark.createDataFrame(data, schemapeople)
df.show(truncate=False)