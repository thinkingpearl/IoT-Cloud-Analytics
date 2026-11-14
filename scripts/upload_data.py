
import os
import csv
import pymysql
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "iot_cleaned.csv"

try:
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO sensor_readings
    (timestamp, sensor_id, temperature, humidity,
     co, lpg, smoke, light, motion)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    batch = []
    count = 0

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            timestamp = row["timestamp"].strip()

            # MySQL DATETIME supports up to 6 fractional digits
            if "." in timestamp:
                timestamp = timestamp[:26]

            values = (
                timestamp,
                row["sensor_id"],
                float(row["temperature"]),
                float(row["humidity"]),
                float(row["co"]),
                float(row["lpg"]),
                float(row["smoke"]),
                row["light"].strip().lower() == "true",
                row["motion"].strip().lower() == "true"
            )

            batch.append(values)

            if len(batch) >= 500:
                cursor.executemany(insert_query, batch)
                count += len(batch)
                batch.clear()

        if batch:
            cursor.executemany(insert_query, batch)
            count += len(batch)

    connection.commit()

    print("DATA UPLOADED SUCCESSFULLY!")
    print("Total records inserted:", count)

except Exception as e:
    if 'connection' in locals():
        connection.rollback()
    print("UPLOAD FAILED:", e)

finally:
    if 'connection' in locals():
        connection.close()
