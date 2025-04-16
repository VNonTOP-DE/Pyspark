from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local[*]").setAppName("Vnontop").set("spark.executor.memory", "4gb")

sc = SparkContext(conf=conf)

data = [
    {"id" : 1, "name" : "vnontop"},
    {"id" : 2, "name" : "son"},
    {"id" : 3, "name" : "tung"},
]

rdd1 = sc.parallelize(data)
rdd2 = sc.parallelize([1,2,3,4,5,6])

rdd3 = rdd1.union(rdd2)
print(rdd3.collect())