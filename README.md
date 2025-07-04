## Data Synchronization Project

### **Overview**

This project, developed from May 2025 to July 2025, provides a robust solution for real-time data synchronization across three databases: MySQL, MongoDB, and Redis. Designed for warehousing applications, it uses MongoDB for deployment and Redis for caching. The system detects schema changes, synchronizes data in near real-time, and includes validation for data accuracy.

### **Features**





- Real-time Synchronization: Ensures data consistency across MySQL, MongoDB, and Redis.



- Change Detection: Uses SQL triggers on MySQL to capture data changes (INSERT, UPDATE, DELETE).



- Data Validation: Verifies data integrity and accuracy across all databases.



- Scalable Architecture: Leverages Apache Spark for data processing and Docker for deployment.

### **Technical Stack**





- Languages: Python



- Frameworks & Tools: Apache Spark, Apache Kafka, Docker



- Libraries:





  - python-cursor



  - pyspark



  - kafka-python



  - mysql-connector-python



  - pymongo



  - redis



-Databases:





  - MySQL (Relational Database)



  - MongoDB (NoSQL Database)



  - Redis (In-memory Cache)

### **Architecture**

The project follows a modular design for real-time data synchronization:

Database Setup:





- MySQL, MongoDB, and Redis are containerized using Docker.



- Configured with secure user credentials and predefined schemas.



- Schema validation ensures consistency across databases.

Data Ingestion:





- Apache Spark inserts data simultaneously into MySQL, MongoDB, and Redis.



- Validation ensures no data is missing and all inserted data is accurate.

Change Detection:





- SQL triggers on MySQL capture INSERT, UPDATE, and DELETE operations.



- Triggered changes are sent to Kafka topics for further processing.

Streaming and Processing:





- Spark Streaming reads change events from Kafka.



- Schema is applied to extract only relevant before-change and after-change data.

Synchronization:





- Spark Streaming applies changes to MongoDB and Redis in near real-time.



- Each modification is validated for accuracy and consistency.

### **Setup Instructions**

Prerequisites





- Docker



- Python 3.8+



- Apache Spark



- Apache Kafka
