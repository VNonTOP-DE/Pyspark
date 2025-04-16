from SparkRDD.Transformation.FileDataSource import file_rdd

upperRdd = file_rdd.map(lambda line: line.upper())

for line in upperRdd.collect():
    print("This is code from map.py")
    print(line)