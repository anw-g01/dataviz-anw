import pandas as pd

# read locations lookup table
locations = pd.read_csv("taxi_zone_lookup.csv")

# standardise column names to lower case
locations.columns = locations.columns.str.lower()

# create a mapping for boroughs only
borough_map = locations.set_index("locationid")["borough"].to_dict()

vendorid_map = {
    1: "Creative Mobile Technologies, LLC",
    2: "Curb Mobility, LLC",
    6: "Myle Technologies Inc",
    7: "Helix"
}

payment_type_map = {
    0: "Flex Fare trip",
    1: "Credit card",
    2: "Cash",
    3: "No charge",
    4: "Dispute",
    5: "Unknown",
    6: "Voided trip"
}

ratecodeid_map = {
    1: "Standard rate",
    2: "JFK",
    3: "Newark",
    4: "Nassau or Westchester",
    5: "Negotiated fare",
    6: "Group ride",
    99: "Null/unknown"
}