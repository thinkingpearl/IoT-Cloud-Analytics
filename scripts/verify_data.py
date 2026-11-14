
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM sensor_readings")
print("Total records:", cursor.fetchone()[0])

cursor.execute("""
SELECT * FROM sensor_readings
ORDER BY id
LIMIT 5
""")

print("\nFirst 5 records:")
for row in cursor.fetchall():
    print(row)

connection.close()
