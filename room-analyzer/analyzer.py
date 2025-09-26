import json
from collections import defaultdict


class DataAnalyzer:
    data: list[dict]

    def __init__(self, data):
        self.data = data
        self.extract_data()

    def analyze(self):
        default_dict = defaultdict(list)
        for offer in self.data:
            default_dict[offer['url']].append(self.get_price(offer))
        return default_dict

    def extract_data(self):
        """Function that cast list of params to dict of params in offer"""
        for offer in self.data:
            offer['params'] = {param['key']: {'name': param['name'], 'value': param['value']} for param in
                               offer['params']}
        return self.data

    def filter_by_params(self, key: str, values: list[str]):
        self.data = [offer for offer in self.data if key in offer['params'] and offer['params'][key]['value']['key'] in values]

    def filter_by_price(self, min_price: int, max_price: int):
        self.data = [offer for offer in self.data if
                     min_price <= int(offer['params']['price']['value']['value']) <= max_price]

    def get_price(self, offer: dict):

        return {
            'title': offer['title'],
            'price': f"{int(offer['params']['price']['value']['value']) +
                        float(offer['params']['rent']['value']['key'])}" if 'rent' in offer[
                'params'] else f"{offer['params']['price']['value']['value']} !!!WITHOUT RENT!!!",
            'url': offer['url']
        }
