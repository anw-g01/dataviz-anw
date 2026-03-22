
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "data" / "taxi_zone_lookup.csv"

# read locations lookup table
locations = pd.read_csv(DATA_PATH)

# standardise column names to lower case
locations.columns = locations.columns.str.lower()

# create a mapping for boroughs only
BOROUGH_MAPPING = locations.set_index("locationid")["borough"].to_dict()

VENDORID_MAPPING = {
    1: "Creative Mobile Technologies, LLC",
    2: "Curb Mobility, LLC",
    6: "Myle Technologies Inc",
    7: "Helix"
}

PAYMENT_TYPE_MAPPING = {
    0: "Flex Fare trip",
    1: "Credit card",
    2: "Cash",
    3: "No charge",
    4: "Dispute",
    5: "Unknown",
    6: "Voided trip"
}

RATECODEID_MAPPING = {
    1: "Standard rate",
    2: "JFK",
    3: "Newark",
    4: "Nassau or Westchester",
    5: "Negotiated fare",
    6: "Group ride",
    99: "Null/unknown"
}