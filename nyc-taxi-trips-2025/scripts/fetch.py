
import pandas as pd
from prepare import prepare_taxi_trips

# https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

def fetch_taxi_data(
        months: list[int] = [6, 7, 8],
        year: int = 2025,
        trip_type: str = "yellow"
) -> dict[str, pd.DataFrame]:

    dfs = {}    # store taxi trips by year-month key

    for i, month in enumerate(months):

        filename = f"{trip_type}_tripdata_{year}-{month:02d}.parquet"
        url = f"{BASE_URL}/{filename}"

        print(f"\rDownloading {i + 1}/{len(months)}: {filename} ...", end="")

        df = pd.read_parquet(url)

        # prepare and store dataset
        dfs[f"{year}-{month:02d}"] = prepare_taxi_trips(df)

    # concatenate all DataFrames
    df = pd.concat(dfs.values(), ignore_index=True)
    print(
        f"\n\ntotal datasets imported: {len(dfs.keys())}"
        f"\ntotal no. of rows: {df.shape[0]:,}"
    )

    return df