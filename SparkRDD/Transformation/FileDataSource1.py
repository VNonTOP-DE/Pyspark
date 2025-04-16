from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local[*]").setAppName("VNonTOP").set("spark.executor.memory", '4g')

sc = SparkContext(conf=conf)

file_rdd = sc.textFile(r"C:\Users\Public\PYSPARK_Python_Learn\SparkRDD\data\data.txt") \
    .map(lambda x: x.lower()) \
    .flatMap(lambda x: x.split(" ")) \
    .map(lambda x: (x, 1)) \
    .reduceByKey(lambda key, value: key + value) \
    .map(lambda x: (x[1], x[0])) \
   .sortByKey(ascending=False)

file_rdd2 = file_rdd.map(lambda x: (x[1], x[0]))
#for i in file_rdd.collect():
 #   print(i)

rdd2 = sc.parallelize([( "to", "your")])
results = file_rdd2.join(rdd2)

print(results.collect())

