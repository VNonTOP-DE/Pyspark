from pyspark import SparkConf, SparkContext
import time

# Config
conf = SparkConf().setMaster("local[*]").setAppName("PartitionBenchmark")
sc = SparkContext(conf=conf)

# Function that simulates a heavy task
def heavy_task(x):
    time.sleep(0.5)  # 0.5 seconds delay per item
    return x * 2

data = list(range(8))  # 8 elements

# 5 Partitions
start_time = time.time()

rdd_5 = sc.parallelize(data, 5)
result_5 = rdd_5.map(heavy_task).collect()

end_time = time.time()
print(f"Time with 5 partitions: {end_time - start_time:.2f} seconds")


# 8 Partitions
start_time = time.time()

rdd_8 = sc.parallelize(data, 8)
result_8 = rdd_8.map(heavy_task).collect()

end_time = time.time()
print(f"Time with 8 partitions: {end_time - start_time:.2f} seconds")

sc.stop()
