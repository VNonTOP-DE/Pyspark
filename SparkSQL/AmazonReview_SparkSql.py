from pyspark.sql import SparkSession
from pyspark.sql.functions import *


spark = SparkSession.builder.appName("vnontop") \
    .master("local[*]").config("spark.executor.memory", "4gb") \
    .getOrCreate()

#read CSV
df = spark.read.csv("C:\\Users\\Public\\PYSPARK_Python_Learn\\SparkSQL\\SparkSqlProject\\amazon_review_data.csv", header=True, inferSchema=True)
df.createOrReplaceTempView("reviews")


df.select(col('*')).show(3)

# Tokenize reviews
tokens_df = df.withColumn("words", explode(split(lower(col("reviewText")), "\\s+")))
tokens_df.createOrReplaceTempView("words")

# Count words per product
spark.sql("""
SELECT asin, words, COUNT(*) AS count
FROM words
WHERE words IN ('broken', 'defective', 'late', 'poor', 'bad', 'damaged')
GROUP BY asin, words
ORDER BY count DESC
""").show()
# AVG Rating by product
spark.sql("""
SELECT asin, AVG(overall) as AVG_Rating
FROM reviews
GROUP BY asin
""").show()