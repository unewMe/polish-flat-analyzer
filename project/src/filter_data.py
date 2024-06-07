import pandas as pd

# Description: Filters out unrealistic data from the list of listings.

# thresholds for filtering unrealistic data
max_price = 5000000  # maximum realistic price
min_price = 10000  # minimum realistic price
max_area = 250  # maximum area in square meters
min_area = 10  # minimum area in square meters
min_floor = 0  # floor
distance_to_city_center = 15  # distance to city center in kilometers


def is_realistic(listing):
    if listing.isnull().any():
        return False

    price = listing['Price']
    area = listing['Area']
    floor = listing['Floor']

    return (min_price <= price <= max_price and
            min_area <= area <= max_area and floor >= min_floor and listing[
                'Distance to city center'] <= distance_to_city_center)


def filter_data(data: pd.DataFrame) -> pd.DataFrame:
    return data[data.apply(is_realistic, axis=1)]
