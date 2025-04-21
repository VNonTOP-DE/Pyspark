import random
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("vnontop") \
    .master("local[*]") \
    .config("spark.executor.memory", "4gb") \
    .getOrCreate()

rdd = spark.sparkContext.parallelize(range(1,11)) \
    .map(lambda x: (x, random.randint(1,99) * x))

#print(rdd.collect())
df = spark.createDataFrame(rdd, ["key", "value"])
df.show()