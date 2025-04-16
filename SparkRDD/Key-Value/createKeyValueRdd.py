from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local[*]").setAppName("vnontop").set("spark.executor.memory","4gb")

sc = SparkContext(conf = conf)

rdd = sc.parallelize([" hom nay toi buon mot minh tren pho dong noi anh den soi sang long lanh"]) \
    .flatMap(lambda x: x.split(" ")) \
    .map(lambda x: (len(x) , x))

groupbykey = rdd.groupByKey()


for key, value in groupbykey.collect():
    print(key, list(value))