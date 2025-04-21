from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("vnontop") \
    .master("local[*]") \
    .config("spark.executor.memory", "4gb") \
    .getOrCreate()

data = [
    ("dat", "DE", 2018),
    ("vnontop", "DS", 2025),
]


df = spark.createDataFrame(data, ["name", "job", "year"])
df.show()