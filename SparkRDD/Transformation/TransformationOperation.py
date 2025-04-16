from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local[*]").setAppName("VNonTOP1").set("spark.executor.memory", '4gb')


sc = SparkContext(conf=conf)

numbers = [1,2,3,4,5,6,7,8,9,10]

numbersRDD = sc.parallelize(numbers)

squaredRdd = numbersRDD.map(lambda s: s*s)
print(squaredRdd.collect())
filterRdd = numbersRDD.filter(lambda x : x>3)
print(filterRdd.collect())
flatmapRdd = numbersRDD.flatMap(lambda vnontop: [vnontop, vnontop*2])
print(flatmapRdd.collect())