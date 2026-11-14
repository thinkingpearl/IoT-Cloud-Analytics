
import pandas as pd
from pathlib import Path

# ---------------------------------------
# 1. Define file locations
# ---------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "iot_raw.csv"
CLEAN_FILE = PROJECT_DIR / "data" / "iot_cleaned.csv"

print("Starting IoT dataset cleaning...")

# ---------------------------------------
# 2. Read original dataset
# ---------------------------------------

df = pd.read_csv(RAW_FILE)

print("\nOriginal dataset information:")
print("Number of records:", len(df))
print("Columns:", df.columns.tolist())

# ---------------------------------------
# 3. Rename columns
# ---------------------------------------

df.rename(columns={
    "ts": "timestamp",
    "device": "sensor_id",
    "temp": "temperature"
}, inplace=True)

# ---------------------------------------
# 4. Convert Unix timestamps
# ---------------------------------------

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    unit="s",
    errors="coerce",
    utc=True
)

# Convert UTC timestamps to timezone-naive
# values for MySQL DATETIME compatibility.
df["timestamp"] = (
    df["timestamp"]
    .dt.tz_localize(None)
)

# ---------------------------------------
# 5. Remove invalid records
# ---------------------------------------

df.dropna(
    subset=["timestamp", "sensor_id"],
    inplace=True
)

# ---------------------------------------
# 6. Convert numerical columns
# ---------------------------------------

numeric_columns = [
    "co",
    "humidity",
    "lpg",
    "smoke",
    "temperature"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# ---------------------------------------
# 7. Remove duplicate records
# ---------------------------------------

original_count = len(df)

df = df.drop_duplicates()

duplicates_removed = original_count - len(df)

# ---------------------------------------
# 8. Standardise data types
# ---------------------------------------

df["sensor_id"] = df["sensor_id"].astype(str)

df["light"] = df["light"].astype(bool)
df["motion"] = df["motion"].astype(bool)

# ---------------------------------------
# 9. Check missing values
# ---------------------------------------

print("\nMissing values:")
print(df.isnull().sum())

# Remove records with missing required fields
df = df.dropna(
    subset=[
        "timestamp",
        "sensor_id",
        "temperature",
        "humidity"
    ]
)

# ---------------------------------------
# 10. Arrange columns
# ---------------------------------------

df = df[
    [
        "timestamp",
        "sensor_id",
        "temperature",
        "humidity",
        "co",
        "lpg",
        "smoke",
        "light",
        "motion"
    ]
]

# ---------------------------------------
# 11. Save cleaned dataset
# ---------------------------------------

df.to_csv(CLEAN_FILE, index=False)

# ---------------------------------------
# 12. Display final results
# ---------------------------------------

print("\nDATA CLEANING COMPLETED!")

print("Original records:", original_count)
print("Duplicate records removed:", duplicates_removed)
print("Final records:", len(df))

print("\nCleaned dataset preview:")
print(df.head())

print("\nCleaned dataset saved at:")
print(CLEAN_FILE)
