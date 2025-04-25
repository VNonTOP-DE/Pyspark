import random

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Quan dz") \
    .getOrCreate()

rdd = spark.sparkContext.parallelize(range(1,11)) \
    .map(lambda x: (x,random.randint(1,1000)*x))

# print(rdd.collect())
schema = ['id','number']
df = spark.createDataFrame(rdd,schema).show()