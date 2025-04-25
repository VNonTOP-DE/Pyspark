import os
os.environ["PYSPARK_PYTHON"] = r"C:\Users\Gap doi den chet\anaconda3\envs\spark_envi3.9\python.exe"
from pyspark import SparkContext, SparkConf
import time
from random import Random
# tạo cấu hình spark
conf = SparkConf().setAppName("My Spark Application").setMaster("local[*]").set("spark.executor.memory", "4g")

sc = SparkContext(conf=conf)

candyTx = sc.parallelize([("candy1", 5.2), ("candy2", 3.5),
                         ("candy1", 2.0), ("candy2", 6.0),
                         ("candy3", 3.0)])

# Reduce by key to sum values for each candy
summaryTx = candyTx.reduceByKey(lambda key, value: key + value )
print(summaryTx.collect())