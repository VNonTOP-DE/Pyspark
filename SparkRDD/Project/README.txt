Project Distributed Data Quality Checker (with PySpark)
🎯 Goal:
Simulate a big dataset of user records.

Check for:

Missing fields (name, age, email)

Invalid ages (age < 0 or > 120)

Invalid emails (not containing @ or malformed)

Count how many bad records there are for each type.

Separate valid and invalid records.

📐 Project Plan
✅ Step 1: Generate Random Data
Each record: { "name": str, "age": int, "email": str }

Include intentional bad data:

Empty names

Ages outside [0, 120]

Invalid emails (like john[at]gmail.com, test.com)

✅ Step 2: Parallelize Data using RDD
Load data into a Spark RDD

✅ Step 3: Data Quality Checks
For each record:

Check 1: Missing name

Check 2: Invalid age

Check 3: Invalid email

Use a function to tag the type of issue for each record.

✅ Step 4: Count Problem Types
Use map and reduceByKey to count:

Number of missing names

Number of invalid ages

Number of invalid emails

✅ Step 5: Split into Valid / Invalid RDDs
Valid RDD: no problems

Invalid RDD: has at least one problem

✅ Step 6 (Optional): Write to CSV/JSON
Save the clean and invalid data separately

