#step 1:Generate Random data
import random
from pyspark import SparkContext,SparkConf
import json
conf = SparkConf().setMaster("local[*]").setAppName("vnontop").set("spark.executor.memory", "4gb")
sc = SparkContext(conf = conf)

def generate_user_data(num_records):
    names = ["John", "Sara", "Mike", "Anna", "Tom", ""]  # Intentionally including empty name
    email_domains = ["@gmail.com", "@yahoo.com", "@outlook.com", ""]

    data = []
    for _ in range(num_records):
        name = random.choice(names)
        age = random.randint(-5, 150)  # Some invalid ages outside [0,120]

        # Randomly mess up emails
        if random.random() < 0.2:
            email = "invalid_email.com"
        else:
            email = name.lower() + random.choice(email_domains)

        record = {"name": name, "age": age, "email": email}
        data.append(record)

    return data


# Example: generate 1000 records
sample_data = generate_user_data(100000)

# Quick preview
#for record in sample_data[:10]:
#   print(record)

#step 2: create function to validate data
def validate_record(record):
    issues = []

    if not record["name"]:
        issues.append("Missing Name")

    if record["age"] < 0 or record["age"] > 120:
        issues.append("Invalid Age")

    if "@" not in record["email"] or record["email"].startswith("@"):
        issues.append("Invalid Email")

    return issues

#step 3: load data generated into RDD

rdd = sc.parallelize(sample_data)
#step 4:  Map records with their validation results
rdd2 = rdd.map(lambda x: (x, validate_record(x)))

#quick check
#for i in rdd2.take(10):
 #   print(i)

#Count problem using Reduce by key

issue_count = rdd2.flatMap(lambda x: x[1]) \
    .map(lambda x: (x,1)) \
    .reduceByKey(lambda x, z : x+z)
### print issue
#for issue, count in issue_count.collect():
#    print(f"{issue}: {count}")

##step 5: Split valid and invalid records
valid_rdd = rdd2.filter(lambda x: len(x[1]) == 0).map(lambda x: x[0])
invalid_rdd = rdd2.filter(lambda x: len(x[1]) > 0).map(lambda x: x[0])

# Count
valid_count = valid_rdd.count()
invalid_count = invalid_rdd.count()

print(f"Valid records: {valid_count}")
print(f"Invalid records: {invalid_count}")

# Convert valid records to JSON strings
valid_json_rdd = valid_rdd.map(lambda record: json.dumps(record))

# Save as text file (each line is a JSON record)
valid_json_rdd.saveAsTextFile("output/valid_records_json")