import json
from collections import defaultdict
from pprint import pprint
from analyzer import DataAnalyzer


def write_into_txt(data):
    with open('Wroclaw.txt', 'w', encoding="utf-8") as f:
        for offer_link, offer_details in data.items():
            f.write(f"Link: {offer_link}\n")
            for offer in offer_details:
                f.write(f"\tTitle: {offer['title']}\n")
                f.write(f"\tPrice: {offer['price']}\n")
            f.write("\n")

def main():
    with open('Warszawa2.json', 'r', encoding='utf-8',errors='ignore') as f:
        data = json.load(f)

    print(len(dict))
    analyzer = DataAnalyzer(data)
    analyzer.filter_by_price(1000, 2600)
    analyzer.filter_by_params('rooms', ['two'])
    result = analyzer.analyze()
    write_into_txt(result)


if __name__ == '__main__':
    main()