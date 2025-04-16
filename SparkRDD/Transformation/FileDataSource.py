from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local[*]").setAppName("VNonTOP").set("spark.executor.memory", '4g')

sc = SparkContext(conf=conf)

file_rdd = sc.textFile(r"C:\Users\Public\PYSPARK_Python_Learn\SparkRDD\data\data.txt")

def main():
    print(file_rdd.collect())
    print(file_rdd.getNumPartitions())
    print(file_rdd.count())
    print(file_rdd.first())
    print(file_rdd.glom().collect())

if __name__ == "__main__":
    main()