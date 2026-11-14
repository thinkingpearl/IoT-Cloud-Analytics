
import os
import pymysql
import matplotlib.pyplot as plt
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

OUTPUT_DIR = "screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# GRAPH 1: Hourly Temperature Trends
cursor.execute("""
SELECT HOUR(timestamp), AVG(temperature)
FROM sensor_readings
GROUP BY HOUR(timestamp)
ORDER BY HOUR(timestamp)
""")

data = cursor.fetchall()
hours = [row[0] for row in data]
temperatures = [float(row[1]) for row in data]

plt.figure(figsize=(10, 5))
plt.plot(hours, temperatures, marker="o")
plt.title("Hourly Average Temperature Trends")
plt.xlabel("Hour of Day")
plt.ylabel("Average Temperature (C)")
plt.xticks(range(24))
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/hourly_temperature.png", dpi=300)
plt.close()


# GRAPH 2: Sensor-wise Average Temperature
cursor.execute("""
SELECT sensor_id, AVG(temperature)
FROM sensor_readings
GROUP BY sensor_id
""")

data = cursor.fetchall()
sensors = [row[0][-8:] for row in data]
temps = [float(row[1]) for row in data]

plt.figure(figsize=(9, 5))
plt.bar(sensors, temps)
plt.title("Sensor-wise Average Temperature")
plt.xlabel("Sensor ID")
plt.ylabel("Temperature (C)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/sensor_temperature.png", dpi=300)
plt.close()


# GRAPH 3: Sensor-wise Average Humidity
cursor.execute("""
SELECT sensor_id, AVG(humidity)
FROM sensor_readings
GROUP BY sensor_id
""")

data = cursor.fetchall()
sensors = [row[0][-8:] for row in data]
humidity = [float(row[1]) for row in data]

plt.figure(figsize=(9, 5))
plt.bar(sensors, humidity)
plt.title("Sensor-wise Average Humidity")
plt.xlabel("Sensor ID")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/sensor_humidity.png", dpi=300)
plt.close()


# GRAPH 4: Light and Motion Analysis
cursor.execute("""
SELECT
    SUM(light = 1),
    SUM(light = 0),
    SUM(motion = 1),
    SUM(motion = 0)
FROM sensor_readings
""")

light_on, light_off, motion_on, motion_off = cursor.fetchone()

categories = ["Light ON", "Light OFF",
              "Motion Detected", "No Motion"]

values = [light_on, light_off, motion_on, motion_off]

plt.figure(figsize=(9, 5))
plt.bar(categories, values)
plt.title("Light and Motion Detection Analysis")
plt.ylabel("Number of Readings")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/light_motion.png", dpi=300)
plt.close()


cursor.close()
connection.close()

print("ALL GRAPHS GENERATED SUCCESSFULLY!")

print("Saved in:", OUTPUT_DIR)
