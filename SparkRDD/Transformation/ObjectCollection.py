from pyspark import SparkContext


sc = SparkContext("local", "VNonTOP")


data = [
    {"id" : 1, "name" : "vnontop"},
    {"id" : 2, "name" : "son"},
    {"id" : 3, "name" : "tung"},
]


rdd = sc.parallelize(data)
print(rdd.collect())