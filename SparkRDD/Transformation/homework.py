#tu mot day so nguyen bat ki, su dung spark de dem so lan xuat hien cua day so nguyen do
import random
from pyspark import SparkContext,SparkConf

conf = SparkConf().setMaster("local[*]").setAppName("vnontop").set("spark.executor.memory", "4gb")

sc = SparkContext(conf = conf)


data =[]

for i in range(500):
    data.append(random.randint(1,50))

rdd = sc.parallelize(data)

rdd1 = rdd.map(lambda x: (x, 1)).reduceByKey(lambda key, value: key + value ) \
    .map(lambda x: (x[1], x[0])) \
    .sortByKey(ascending=False)
print(rdd.collect())
for i in rdd1.collect():
    print(i)
distinct_count = rdd1.count()
print(f"Distinct numbers in data: {distinct_count}")
