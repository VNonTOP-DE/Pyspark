from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("vnontop").master("local[*]").config("spark.executor.memory", "4gb") \
    .getOrCreate()

textFile = spark.read.text("C:\\Users\\Public\\PYSPARK_Python_Learn\\StudyData\\text.txt")

textFile.show()