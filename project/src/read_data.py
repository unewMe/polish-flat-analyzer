import pandas as pd
import json


def read_data(file_path: str) -> pd.DataFrame | None:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        processed_data = []
        for offer in data:
            offer_params = offer.get('params', [])
            location = offer.get('location', {})
            temp_dict = {}
            temp_dict['Location'] = location.get('city', {}).get('name', None)
            for param in offer_params:
                if param['key'] == 'price':
                    temp_dict[param['name']] = param['value']['value']
                else:
                    temp_dict[param['name']] = param['value'].get('key', None)

            processed_data.append(temp_dict)

        processed_data = pd.DataFrame(processed_data)
        processed_data.rename(
            columns={'Powierzchnia': 'Area', 'Liczba pokoi': 'Rooms', 'Rynek': 'Market', 'Poziom': 'Floor',
                     'Rodzaj zabudowy': 'Building type', 'Umeblowane': 'Furnished', 'Cena': 'Price',
                     'Cena za m²': 'Price per m'}, inplace=True)
        return processed_data

    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None


if __name__ == '__main__':
    df = read_data('../../data/Warszawa.json')
    df = df['Rynek'].unique()
    df = list(df)
    print(df)
