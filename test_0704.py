from pyspark import SparkContext, SparkConf
import time
from random import Random
# tạo cấu hình spark
conf = SparkConf().setAppName("Spark Application").setMaster("local[*]").set("spark.executor.memory", "4g")

sc = SparkContext(conf=conf)

numberRdd = sc.parallelize([1,2,3,4,5,6,7,8,9,10],2)

def add(v1: int, v2: int) -> int:
    print(f"v1: {v1}, v2: {v2} => ({v1 + v2})")
    return v1 + v2
print(numberRdd.reduce(add))