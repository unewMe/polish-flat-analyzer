import pandas as pd

# Description: Filters out unrealistic data from the list of listings.

# thresholds for filtering unrealistic data
max_price = 1000000  # maximum realistic price
min_price = 10000  # minimum realistic price
max_price_per_m2 = 20000  # maximum price per square meter
min_price_per_m2 = 2000  # minimum price per square meter
max_area = 200  # maximum area in square meters
min_area = 10  # minimum area in square meters
min_floor = 0  # floor


def is_realistic(listing):
    if listing.isnull().any():
        return False

    price = float(listing['Price'])
    area = float(listing['Area'])
    price_per_m2 = float(listing['Price per m'])
    floor = int(listing['Floor'])

    return (min_price <= price <= max_price and
            min_area <= area <= max_area and
            min_price_per_m2 <= price_per_m2 <= max_price_per_m2 and floor >= min_floor)


def filter_data(data: pd.DataFrame) -> pd.DataFrame:
    return data[data.apply(is_realistic, axis=1)]
