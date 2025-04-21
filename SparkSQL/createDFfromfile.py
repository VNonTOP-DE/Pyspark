from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("vnontop") \
    .config("spark.executor.memory", "4gb") \
    .master("local[*]") \
    .getOrCreate()

jsondata = spark.read.json("C:\\Users\\Public\\PYSPARK_Python_Learn\\StudyData\\2015-03-01-17.json")
jsondata.show(5)