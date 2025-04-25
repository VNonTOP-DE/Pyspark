### Seperate Date Data into 3 columns  for Year, Month and Day
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

#set up Spark
spark = SparkSession.builder.appName("vnontop").master("local[*]") \
    .config("spark.executor.memory", "4gb").getOrCreate()

#data
data = [
    ["23/04.2025"],
    ["~11-01//2021"],
    ["2021--/.09*30"],
    ["2025*12@01"],
    ["04~05~2023"],
    ["1999#7#13"],
    ["30|6|2001"],
    ["2000**10**09"],
    ["8.9.2022"],
    ["2024--1--5"]
]
#Create dataframe from data
df = spark.createDataFrame(data, ["date"])

#Use regexp_replace to replace all special characters to ' '
df_removeSC = df.withColumn("cleaned", regexp_replace(col("date"), "[^0-9]", " "))

#Use strim to remove extra ' '
#Split day,month,year by one or more ' ' in a new column
tokens_df = df_removeSC.withColumn("tokens", split(trim(col("cleaned")), "\\s+"))


#check result
#df_removeSC.select(col("cleaned")).show(truncate=False)
#tokens_df.select(col("tokens")).show(truncate=False)

#identify which is year by length of words
tokens_df = tokens_df.withColumn("year",
    expr("CASE WHEN length(tokens[0]) = 4 THEN tokens[0] ELSE tokens[2] END")
)
#tokens_df.select(col("year")).show(truncate=False)

#apply the same logic to find day
#day will on the other side of year
tokens_df = tokens_df.withColumn("day",
    expr("CASE WHEN length(tokens[0]) = 4 THEN tokens[2] ELSE tokens[0] END")
)

#create month column
#with international date format, moth always in the middle
tokens_df = tokens_df.withColumn("month", col("tokens")[1])


#print result
tokens_df.select("year", "month", "day", "cleaned", "tokens", "date").show(truncate=False)

