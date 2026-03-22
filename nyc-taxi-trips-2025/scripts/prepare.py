
import pandas as pd 
import lookup   # get mapping dictionaries


def prepare_taxi_trips(df: pd.DataFrame) -> pd.DataFrame:
    """Clean, process, and prepare a NYC Taxi Trips dataset for a gven month."""

    # standardise all column names to lowercase
    df.columns = df.columns.str.lower()

    # return the cleaned and processed DataFrame
    return (

        df

        # filter out invalid/unexpected values
        .loc[
            lambda x:
            (x["fare_amount"] >= 0) &
            (x["total_amount"] >= 0) &
            (x["tip_amount"] >= 0) 
        ]

        # rename columns
        .rename(
            columns={
                "tpep_pickup_datetime": "pickup_datetime",
                "tpep_dropoff_datetime": "dropoff_datetime",
                "pulocationid": "pickup_location_id",
                "dolocationid": "dropoff_location_id"
            }
        )

        # drop unwanted columns
        .drop(
            columns=[
                "store_and_fwd_flag",
                "improvement_surcharge",
                "mta_tax", "tolls_amount",
                "extra", "airport_fee",
                "cbd_congestion_fee",
                "congestion_surcharge"
            ]
        )

        # create new columns
        .assign(

            # trip dates and times
            pickup_date=lambda x: x["pickup_datetime"].dt.date,
            pickup_time=lambda x: x["pickup_datetime"].dt.time,
            pickup_hour=lambda x: x["pickup_datetime"].dt.hour,
            pickup_month=lambda x: x["pickup_datetime"].dt.month_name().astype("category"),   

            # weekday name and ordering
            pickup_weekday=lambda x: pd.Categorical(
                x["pickup_datetime"].dt.day_name(),
                categories=[
                    "Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"
                ],
                ordered=True
            ),

            # trip durations
            duration_secs=lambda x: (x["dropoff_datetime"] - x["pickup_datetime"]).dt.total_seconds(),
            duration_mins=lambda x: x["duration_secs"] / 60,
            duration_hours=lambda x: x["duration_mins"] / 60,

            # apply code mappings (see data dictionary)
            vendorid=lambda x: x["vendorid"].map(lookup.VENDORID_MAPPING).astype("category"),
            payment_type=lambda x: x["payment_type"].map(lookup.PAYMENT_TYPE_MAPPING).astype("category"),
            ratecodeid=lambda x: x["ratecodeid"].map(lookup.RATECODEID_MAPPING).astype("category"),

            # create location mappings from lookup table 
            pickup_borough=lambda x: x["pickup_location_id"].map(lookup.BOROUGH_MAPPING).astype("category"),
            dropoff_borough=lambda x: x["dropoff_location_id"].map(lookup.BOROUGH_MAPPING).astype("category"),

            # flags
            tipped=lambda x: x["tip_amount"] > 0,
            same_borough=lambda x: x["pickup_borough"] == x["dropoff_borough"]
        )

        # drop location ID columns
        .drop(columns=["pickup_location_id", "dropoff_location_id"])

        # optional
        .sort_values(by="pickup_datetime")
        .reset_index(drop=True)
    )