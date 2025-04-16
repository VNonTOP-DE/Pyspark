from os import remove
from re import split

from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local[*]").setAppName("vnontop").set('spark.executor.memory', '4gb')


sc = SparkContext(conf=conf)

text = sc.parallelize(["Tomorrow is ChummyCat's birthday"]) \
        .map(lambda x: x.lower()) \
        .flatMap(lambda x: x.split(" "))

removetext = sc.parallelize(["is", "tomorrow"])

result = text.subtract(removetext)
print(result.collect())
