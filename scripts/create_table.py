
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
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        sensor_id VARCHAR(100),
        temperature FLOAT,
        humidity FLOAT,
        co FLOAT,
        lpg FLOAT,
        smoke FLOAT,
        light BOOLEAN,
        motion BOOLEAN
    );
    """

    cursor.execute(create_table_query)
    connection.commit()

    print("TABLE CREATED SUCCESSFULLY!")
    print("Table name: sensor_readings")

    cursor.close()
    connection.close()

except Exception as e:
    print("ERROR:", e)
