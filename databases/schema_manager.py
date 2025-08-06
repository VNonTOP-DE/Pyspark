from pathlib import Path
from tkinter.tix import Select
from traceback import print_tb

from mysql.connector import Error



SQL_FILE_PATH = Path("../sql/schema.sql")




def create_mysql_schema(connection, cursor):
    database = "github_data"
    cursor.execute(f"DROP DATABASE IF EXISTS {database}")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    connection.commit()
    print(f"-----------------CREATE {database} SUCCESS------------------")
    connection.database = database
    try:
        with open(SQL_FILE_PATH, "r") as file:
            sql_script = file.read()
            sql_commmands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]

            for cmd in sql_commmands:
                cursor.execute(cmd)
                print(f"-------------Executed mysql command-----------------")
    except Error as e:
        connection.rollback()
        raise Exception(f"-------------Failed to Create Mysql Schema: {e}----------") from e



def validate_mysql_schema(cursor):
    cursor.execute("SHOW TABLES")
    table_list = cursor.fetchall()
    tables = [row[0] for row in table_list]
    #print(tables)
    if "users" not in tables or "repositories" not in tables:
        raise ValueError(f"========= table doestn't exist =============")
    #print("-------------------validate success------------------")

    cursor.execute("SELECT * FROM users WHERE user_id = 1")
    user = cursor.fetchall()
    if not user:
        raise ValueError("---------------user not found--------")
    print("-----------validate schema in mysql success--------")


def create_mongodb_schema(db):
    db.drop_collection("users")
    db.create_collection("users", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id","login"],
            "properties": {
                "user_id": {
                    "bsonType": "int"
                },
                "login": {
                    "bsonType": "string"
                },
                "gravatar_id": {
                    "bsonType": "string"
                },
                "url": {
                    "bsonType": "string"
                },
                "avatar_url": {
                    "bsonType": "string"
                }
            }
        }
    })
    # Create a unique index on the user_id field
    db["users"].create_index("user_id", unique=True)
    print("-------------created Collection Users in MongoDB---------------")



def validate_mongodb_schema(db):
    collections = db.list_collection_names()
    #print(f"-----------collection: {collections}-------------")
    if "users" not in collections:
        raise ValueError(f"------Collection in MongoDB doesn't exist-----")
    user = db.users.find_one({"user_id" : 1})
    #print(user)
    if not user:
        raise ValueError(f"----------user_id not found in MongoDB----------")
    print("--------------validate schema in mongoDB success--------")
