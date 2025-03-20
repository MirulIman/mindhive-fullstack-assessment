import googlemaps
import pymysql
import pandas as pd
import os
import time
from src.database import get_db_connection
from src.config import GOOGLE_MAPS_API_KEY

# Ensure 'data' folder exists
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

csv_file_path = os.path.join(data_folder, "subway_outlets.csv")

conn = get_db_connection()
cursor = conn.cursor(pymysql.cursors.DictCursor)

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

df = pd.read_csv(csv_file_path)
df.columns = df.columns.str.strip().str.lower()

if "latitude" not in df.columns:
    df["latitude"] = None
if "longitude" not in df.columns:
    df["longitude"] = None

missing_geo = df[df["latitude"].isna() | df["longitude"].isna()]

for index, row in missing_geo.iterrows():
    address = row["address"]
    try:
        gmaps_result = gmaps.geocode(address)
        if gmaps_result:
            lat = gmaps_result[0]["geometry"]["location"]["lat"]
            lon = gmaps_result[0]["geometry"]["location"]["lng"]
            
            cursor.execute("""
                UPDATE outlets 
                SET latitude = %s, longitude = %s 
                WHERE name = %s AND address = %s
            """, (lat, lon, row["name"], row["address"]))
            conn.commit()
            df.at[index, "latitude"] = lat
            df.at[index, "longitude"] = lon

        time.sleep(0.5)
    except Exception as e:
        print(f"Error geocoding {address}: {e}")

cursor.close()
conn.close()
df.to_csv(csv_file_path, index=False, encoding="utf-8")
print("Geocoding completed and data updated.")
