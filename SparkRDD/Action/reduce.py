from pyspark import SparkContext,SparkConf

conf= SparkConf().set("spark.executor.memory", "4gb").setAppName("vnontop").setMaster("local[*]")

sc = SparkContext(conf = conf)

data = sc.parallelize([1,2,3,4,5,6,7,8,9,10], 5)

def sum(x1: int, x2: int) ->int:
    print(f"x1 : {x1}, x2: {x2} => ({x1} + {x2})")
    return x1 + x2

print(data.reduce(sum))
