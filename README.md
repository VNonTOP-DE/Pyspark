# Pyspark
Pyspark Course by DatDang
Bai toan dong bo du lieu | sử dụng MySQL làm nguồn dữ liệu chính, kết hợp với Kafka và Spark để xử lý và đồng bộ dữ liệu sang MongoDB và Redis.

step 1: install Docker

open powershell:
docker run -p 3307:3306 --name=mysql1 -d --restart unless-stopped mysql/mysql-server:latest
docker logs mysql1 2>&1 | grep GENERATED
docker exec -it mysql1 mysql -uroot -p
It will show Enter password: then you click right mount (it is paste) and hit enter (control + V then Enter will not work)

try mysql> SHOW DATABASES
if ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.
then 
ALTER USER 'root'@'localhost' IDENTIFIED BY '123';
-----------------------------
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=vnontop \
  -e MONGO_INITDB_ROOT_PASSWORD=123 \
  mongo:latest

  docker exec -it mongodb mongosh -u vnontop -p 123
  -----------------------------------------------------------
  Data Synchronization Project
Overview
This project, developed from May 2025 to July 2025, provides a robust solution for real-time data synchronization across three different databases: MySQL, MongoDB, and Redis. The system ensures seamless data consistency for warehousing applications, with MongoDB used for deployment and Redis for caching. It includes schema change detection, streamlined synchronization, and validation for data accuracy.
Features

Real-time Synchronization: Synchronizes data across MySQL, MongoDB, and Redis in near real-time.
Change Data Capture (CDC): Detects and propagates schema changes and data modifications using Debezium and Kafka.
Data Validation: Ensures data integrity and accuracy across all databases.
Scalable Architecture: Leverages Spark for data processing and streaming, with Docker for easy deployment.

Technical Stack

Languages: Python
Frameworks & Tools: Apache Spark, Debezium, Apache Kafka, Docker
Libraries:
python-cursor
pyspark
kafka-python
mysql-connector-python
pymongo
redis


Databases:
MySQL (Relational Database)
MongoDB (NoSQL Database)
Redis (In-memory Cache)



Architecture
The project follows a modular architecture to achieve real-time data synchronization:

Database Setup:

MySQL, MongoDB, and Redis are containerized using Docker.
Configured with secure user credentials and predefined schemas.
Schema validation ensures consistency across databases.


Data Ingestion:

Apache Spark is used to insert data simultaneously into MySQL, MongoDB, and Redis.
Validation checks ensure no data is missing and all inserted data is accurate.


Change Data Capture (CDC):

Debezium monitors MySQL for changes (INSERT, UPDATE, DELETE) and streams them to Kafka topics.


Streaming and Processing:

Spark Streaming reads change events from Kafka.
Schema is applied to extract only relevant before-change and after-change data.


Synchronization:

Spark Streaming applies changes to MongoDB and Redis in near real-time.
Each modification is validated to ensure accuracy and consistency.



Setup Instructions
Prerequisites

Docker
Python 3.8+
Apache Spark
Apache Kafka
Debezium

Installation

Clone the Repository:
git clone https://github.com/<your-username>/data-synchronization.git
cd data-synchronization


Set Up Docker:

Start the Docker containers for MySQL, MongoDB, Redis, and Kafka:docker-compose up -d




Install Python Dependencies:
pip install -r requirements.txt


Configure Environment Variables:

Create a .env file based on .env.example and update database credentials and Kafka settings.


Run the Application:

Start the Spark job for data ingestion and synchronization:spark-submit src/main.py





