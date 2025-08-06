def spark_write_mysql_primaryKey(self, df: DataFrame, jdbc_url: str, config: Dict, mode: str = "append"):
    df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", "spark_table_temp") \
        .option("user", config["user"]) \
        .option("password", config["password"]) \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .mode(mode) \
        .save()

    print(f"-----spark write data to mysql table: spark_table_temp successfully-------")


def validate_spark_write_primaryKey(self, df_write: DataFrame, jdbc_url: str, config: Dict,
                                    mode: str = "append"):
    try:
        df_read = self.spark.read \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", "spark_table_temp") \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .load()
        # df_read.show()
        df_temp = df_write.exceptAll(df_read)
        # print(df_temp.count())
        if df_temp.count() != 0:
            df_temp.write \
                .format("jdbc") \
                .option("url", jdbc_url) \
                .option("dbtable", "spark_table_temp") \
                .option("user", config["user"]) \
                .option("password", config["password"]) \
                .option("driver", "com.mysql.cj.jdbc.Driver") \
                .mode(mode) \
                .save()
        print(f"-------validate spark write data to mysql table spark_table_temp successfully------")
    except Exception as e:
        raise Exception(f"----failed to write missing record to spark_table_temp in mysql----")


def insert_data_mysql_primaryKey(self, config: Dict):
    try:
        with MySQLConnect(config["host"], config["port"], config["user"],
                          config["password"]) as mysql_client:
            connection, cursor = mysql_client.connection, mysql_client.cursor
            database = get_database_config()["mysql"].database
            connection.database = database
            cursor.execute(
                "SELECT a. * FROM spark_table_temp a LEFT JOIN users b ON a.user_id = b.user_id WHERE b.user_id IS NULL;")
            records = []
            row = cursor.fetchone()

            while row:
                records.append(row)
                row = cursor.fetchone()

            for rec in records:
                try:
                    cursor.execute(
                        "INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (%s, %s, %s, %s, %s)",
                        rec
                    )
                    connection.commit()
                    print("-----insert data into mysql successfully-----")
                except Exception as e:
                    print(f"Error inserting record {rec}: {str(e)}")
                    continue

    except Exception as e:
        raise Exception(f"-----failed to connect to mysql: {e}------")