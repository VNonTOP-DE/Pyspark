from pyspark import SparkContext, SparkConf
import time
from random import random, Random

conf = SparkConf().setMaster("local[*]").setAppName("VNonTOP2").set("spark.executor.memory", '4gb')

sc = SparkContext(conf=conf)

data = ['Vnontop', 'Quynh' , 'Dung' , 'Khanh']

rdd = sc.parallelize(data, 2)
#print(rdd.glom().collect())
"""
def process_partition(iterator):
    rand = Random(int(time.time() * 1000) + Random().randint(0, 1000))
    return [f"{name} : {rand.randint(0, 1000)}" for name in iterator]
"""

results = rdd.mapPartitions(
    lambda iterator : map(
        lambda name: f"{name} : {Random(int(time.time() * 1000) + Random().randint(0, 1000)).randint(0, 1000)}", iterator
    )
)
print(results.collect())