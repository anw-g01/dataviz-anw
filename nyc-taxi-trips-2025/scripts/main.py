
from pathlib import Path
from fetch import fetch_taxi_data

BASE_DIR = Path(__file__).resolve().parent

# fetch taxi data from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

df = fetch_taxi_data()

# export to CSV and/or Parquet

df.to_parquet(BASE_DIR.parent / "data" / "taxi-trips-summer.parquet", index=False)
df.to_csv(BASE_DIR.parent / "data" / "taxi-trips-summer.csv", index=False)