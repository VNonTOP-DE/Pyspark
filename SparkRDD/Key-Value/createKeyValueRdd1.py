from pyspark import SparkContext, SparkConf

conf = SparkConf().set("spark.executor.memory" , "4gb").setAppName("vnontop").setMaster("local[*]")

sc = SparkContext(conf=conf)


data = sc.parallelize([
    ("vietanh", 15), ("huyquang", 20),
    ("vietanh", 3), ("dat", 30),
    ("huyquang", 10)
])

results = data.reduceByKey(lambda key, value : key + value)


data2 = sc.parallelize([
    ("vietanh", "depzai"), ("huyquang", "depgai"),
    ("vietanh", "DE"), ("dat", "DA"),
    ("huyquang", "DS"), ("dat", "depzai")
])

data3 = data.join(data2).sortByKey(ascending=False)


for i in data3.collect():
    print(i)
