from pyspark import SparkContext,SparkConf

conf= SparkConf().set("spark.executor.memory", "4gb").setAppName("VNonTOP").setMaster("local[*]")


sc = SparkContext(conf = conf)

data = sc.parallelize(["one", "two", "three", "four", "Two", "FOUR", 1 , 1, 4,5,6,4,2,5,3,2,65,6,2])

transData = data.distinct()

print(transData.collect())