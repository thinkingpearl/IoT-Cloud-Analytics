
import os
import pandas as pd
import pymysql
from dotenv import load_dotenv

load_dotenv()

# Read cleaned dataset
df = pd.read_csv("iot_cleaned.csv")

connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = connection.cursor()

query = """
INSERT INTO sensor_readings
(timestamp, sensor_id, temperature, humidity,
co, lpg, smoke, light, motion)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

data = [
    tuple(None if pd.isna(v) else v for v in row)
    for row in df.itertuples(index=False, name=None)
]

batch_size = 5000

for i in range(0, len(data), batch_size):
    cursor.executemany(query, data[i:i + batch_size])
    connection.commit()
    print(f"Inserted {min(i + batch_size, len(data))}/{len(data)} records")

cursor.close()
connection.close()

print("DATA UPLOADED SUCCESSFULLY!")
