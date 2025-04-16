from pyspark import SparkContext, SparkConf

conf = SparkConf().set("spark.executor.memory", "4gb").setMaster("local[*]").setAppName("vnonotp")

sc = SparkContext(conf=conf)

rdd1 = sc.parallelize([1,2,3,4,5,6,7])
rdd2 = sc.parallelize([1,2,7,8,9,10])

intersection = rdd1.intersection(rdd2)
print(intersection.collect())