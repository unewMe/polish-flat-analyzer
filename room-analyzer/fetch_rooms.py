import requests
import json
import os
from collections import defaultdict
import time


API_URL = "https://www.olx.pl/api/v1/offers"
BASE_API = "https://www.olx.pl/api/v1"
ALLOWED_CITIES = {"Warszawa": 17871, "Kraków": 8959, "Gdańsk": 5659, "Wrocław": 19701, "Białystok": 1079,
                  "Bydgoszcz": 4019, "Gorzów Wielkopolski": 6331, "Katowice": 7691, "Kielce": 7971, "Lublin": 10119,
                  "Łódź": 10609, "Olsztyn" : 12673, "Opole" : 12885,"Poznań" : 13983, "Rzeszów" : 15241, "Szczecin" : 16705, "Toruń" : 38395, "Zielona Góra" : 20787}

SORT_OPTIONS = {
    "Oldest": "created_at:asc",
    "Newest": "created_at:desc",
}


def fetch_data(url: str) -> dict:
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return {}


def list_offers(options: dict) -> dict:
    query_params = {k: str(v) for k, v in options.items() if v is not None}  # Ensure None values are not included
    response = fetch_data(f"{API_URL}?{requests.utils.unquote(requests.compat.urlencode(query_params))}")

    # Organize offers by city
    if 'data' in response:
        offers_by_city = defaultdict(list)
        for offer in response['data']:
            city_name = offer['location']['city']['name']
            offers_by_city[city_name].append(offer)
        return offers_by_city
    else:
        raise FileExistsError("End")


def add_offers(existing_offers: list, new_offers: list) -> list:
    existing_ids = {offer['id'] for offer in existing_offers}
    new_offers = [offer for offer in new_offers if offer['id'] not in existing_ids]
    return existing_offers + new_offers


def save_offers_by_city(offers_by_city: dict):
    for city, offers in offers_by_city.items():
        if city in ALLOWED_CITIES:
            file_name = f"{city.replace(' ', '_')}.json"
            if os.path.exists(file_name):
                with open(file_name, 'r', encoding='utf-8') as f:
                    existing_offers = json.load(f)
                combined_offers = add_offers(existing_offers, offers)
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(combined_offers, f, ensure_ascii=False, indent=4)
                print(f"Appended {len(offers)} offers to {file_name}")
            else:
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(offers, f, ensure_ascii=False, indent=4)
                print(f"Saved {len(offers)} offers to {file_name}")


def update_offers(sort_by: str = "created_at:desc", city_id: int = 0):
    start(sort_by, city_id, False)


def start(sort_by: str, city_id: int, inifinite: bool = True):
    options = {
        'offset': 0,
        'limit': 40,
        'category_id': 15,
        'sort_by': sort_by,
        'city_id': city_id
    }

    while inifinite:
        try:
            offers_by_city = list_offers(options)
            if offers_by_city:
                save_offers_by_city(offers_by_city)
            options['offset'] += options['limit']
            time.sleep(5)

        except FileExistsError:
            break


def main():
    for sorting in SORT_OPTIONS.values():
        for city_id in ALLOWED_CITIES.values():
            start(sorting, city_id)


if __name__ == "__main__":
    start("created_at:desc", 19701)
    start("created_at:asc", 19701)
