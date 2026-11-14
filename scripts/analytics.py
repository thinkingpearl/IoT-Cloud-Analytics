
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

# Connect to AWS RDS
connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = connection.cursor()

print("=" * 60)
print("       IoT CLOUD ANALYTICS SYSTEM")
print("=" * 60)

# 1. Total sensor readings
print("\n1. TOTAL SENSOR READINGS")

cursor.execute("""
SELECT COUNT(*) FROM sensor_readings
""")

print("Total records:", cursor.fetchone()[0])


# 2. Temperature analysis
print("\n2. TEMPERATURE ANALYSIS")

cursor.execute("""
SELECT
    ROUND(AVG(temperature), 2),
    ROUND(MIN(temperature), 2),
    ROUND(MAX(temperature), 2)
FROM sensor_readings
""")

avg_temp, min_temp, max_temp = cursor.fetchone()

print("Average Temperature:", avg_temp)
print("Minimum Temperature:", min_temp)
print("Maximum Temperature:", max_temp)


# 3. Humidity analysis
print("\n3. HUMIDITY ANALYSIS")

cursor.execute("""
SELECT
    ROUND(AVG(humidity), 2),
    ROUND(MIN(humidity), 2),
    ROUND(MAX(humidity), 2)
FROM sensor_readings
""")

avg_humidity, min_humidity, max_humidity = cursor.fetchone()

print("Average Humidity:", avg_humidity)
print("Minimum Humidity:", min_humidity)
print("Maximum Humidity:", max_humidity)


# 4. Gas sensor analysis
print("\n4. GAS SENSOR ANALYSIS")

cursor.execute("""
SELECT
    ROUND(AVG(co), 6),
    ROUND(AVG(lpg), 6),
    ROUND(AVG(smoke), 6)
FROM sensor_readings
""")

avg_co, avg_lpg, avg_smoke = cursor.fetchone()

print("Average CO:", avg_co)
print("Average LPG:", avg_lpg)
print("Average Smoke:", avg_smoke)


# 5. Light and motion detection
print("\n5. LIGHT AND MOTION DETECTION")

cursor.execute("""
SELECT
    SUM(light = 1),
    SUM(motion = 1),
    SUM(light = 0),
    SUM(motion = 0)
FROM sensor_readings
""")

light_on, motion_detected, light_off, no_motion = cursor.fetchone()

print("Light ON:", light_on)
print("Motion Detected:", motion_detected)
print("Light OFF:", light_off)
print("No Motion:", no_motion)


# 6. Sensor-wise analysis
print("\n6. SENSOR-WISE ANALYSIS")

cursor.execute("""
SELECT
    sensor_id,
    COUNT(*) AS total_readings,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(AVG(humidity), 2) AS avg_humidity
FROM sensor_readings
GROUP BY sensor_id
ORDER BY total_readings DESC
""")

for row in cursor.fetchall():
    print(row)


# 7. Hourly temperature trends
print("\n7. HOURLY TEMPERATURE TRENDS")

cursor.execute("""
SELECT
    HOUR(timestamp) AS reading_hour,
    COUNT(*) AS total_readings,
    ROUND(AVG(temperature), 2) AS avg_temperature
FROM sensor_readings
GROUP BY HOUR(timestamp)
ORDER BY reading_hour
""")

for row in cursor.fetchall():
    print(row)


print("\n" + "=" * 60)
print("       ANALYTICS COMPLETED SUCCESSFULLY")
print("=" * 60)

cursor.close()
connection.close()
