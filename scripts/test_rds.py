
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

try:
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        connect_timeout=10
    )

    print("AWS RDS CONNECTION SUCCESSFUL!")

    connection.close()

except Exception as e:
    print("CONNECTION FAILED:")
    print(e)
