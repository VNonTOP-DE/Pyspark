
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("vnontop") \
    .config("spark.executor.memory", "4gb") \
    .master("local[*]") \
    .getOrCreate()


data = spark.sparkContext.parallelize([
    Row(1, "dat", 18),
    Row(2, "vnontop", 25),
])


schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("name", StringType(), True),
    StructField("year", LongType(), True),
])

df = spark.createDataFrame(data, schema)
df.show()

"""
Data Type | Description
StringType | Represents string/text values.
IntegerType | Represents 32-bit integer numbers.
LongType | Represents 64-bit long integer numbers.
FloatType | Represents 32-bit floating-point numbers (decimal numbers).
DoubleType | Represents 64-bit floating-point numbers (higher precision).
ShortType | Represents 16-bit integer numbers.
ByteType | Represents 8-bit integer numbers.
BooleanType | Represents True or False values.
DecimalType | Represents fixed-precision decimals, good for financial data.
DateType | Represents a date without time (YYYY-MM-DD).
TimestampType | Represents a timestamp (date + time + timezone).
BinaryType | Represents binary data (like images, files).
ArrayType | Represents an array (list) of values of a specified type.
MapType | Represents a dictionary with keys and values of specified types.
StructType | Represents a complex structure, like a table or JSON object.
StructField | Represents a single field inside a StructType.
"""