import pandas as pd
import json
from .location_measure import get_distance_to_city_center

EXCEPT_PARAMS = ['Cena za m²']


def read_data(file_path: str) -> pd.DataFrame | None:
    """Reads the data from the json file and returns it as a DataFrame. Also calculates the distance to the city center and drops the unnecessary columns."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        rd_data = []
        for offer in data:
            offer_params = offer.get('params', [])
            location = offer.get('location', {})
            map = offer.get('map', {})
            temp_dict = {}
            temp_dict['City'] = location.get('city', {}).get('name', None)
            for param in offer_params:
                if param['key'] == 'price':
                    temp_dict[param['name']] = param['value']['value']
                else:
                    temp_dict[param['name']] = param['value'].get('key', None)

            temp_dict = {k: v for k, v in temp_dict.items() if k not in EXCEPT_PARAMS}

            temp_dict['Distance to city center'] = get_distance_to_city_center(city=temp_dict['City'],
                                                                               lat=map.get('lat', None),
                                                                               lon=map.get('lon', None))

            rd_data.append(temp_dict)

        rd_data = pd.DataFrame(rd_data)
        rd_data = rd_data.dropna()
        rd_data.rename(
            columns={'City': 'City', 'Powierzchnia': 'Area', 'Liczba pokoi': 'Rooms', 'Rynek': 'Market',
                     'Poziom': 'Floor',
                     'Rodzaj zabudowy': 'Building type', 'Umeblowane': 'Furnished', 'Cena': 'Price',
                     'Distance to city center': 'Distance to city center'}, inplace=True)
        rd_data['Area'] = rd_data['Area'].astype(float)

        return rd_data

    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None


if __name__ == '__main__':
    df = read_data('../../data/data.json')
    print(df)
