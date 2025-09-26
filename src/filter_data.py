import pandas as pd
from project.src.process_data import Preprocessor

# Description: Filters out unrealistic data from the list of listings.

# thresholds for filtering unrealistic data
max_price = 5000000  # maximum realistic price
min_price = 10000  # minimum realistic price
max_area = 250  # maximum area in square meters
min_area = 10  # minimum area in square meters
min_floor = 0  # minimum floor
distance_to_city_center = 15  # distance to city center in kilometers


def is_realistic(listing: pd.Series) -> bool:
    """Checks if the listing is realistic based on the thresholds."""

    if listing.isnull().any():
        return False

    price = listing['Price']
    area = listing['Area']
    floor = listing['Floor']
    distance = listing['Distance to city center']

    return (min_price <= price <= max_price and
            min_area <= area <= max_area and int(floor) >= min_floor and distance <= distance_to_city_center)


def filter_data(data: pd.DataFrame) -> pd.DataFrame:
    """Filters out unrealistic data from the list of listings."""
    new_data = data[data.apply(is_realistic, axis=1)]
    return new_data.dropna()


def filter_preprocessor(preprocessor: Preprocessor) -> None:
    """Filters out unrealistic data from the preprocessor."""
    filtered_data = filter_data(preprocessor.decode_data(preprocessor.preprocessed_data.copy()))
    preprocessor.preprocessed_data = preprocessor.encode_data(filtered_data)
