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

