from pyspark import SparkContext, SparkConf

conf = SparkConf().set("spark.executor.memory" , "4gb").setAppName("vnontop").setMaster("local[*]")

sc = SparkContext(conf=conf)


data = sc.parallelize([
    ("vietanh", 15), ("huyquang", 20),
    ("vietanh", 3), ("dat", 30),
    ("huyquang", 10)
])

data2 = data.reduceByKey(lambda total, value : total + value)


data3 = data2.map(lambda x: (x[1], x[0])).sortByKey(ascending=False)

print(data3.collect())