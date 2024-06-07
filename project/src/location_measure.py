import math

city_center_coordinates = {"Warszawa": {"lat": 52.231816, "lon": 21.006259},
                           "Wrocław": {"lat": 51.108443, "lon": 17.040535},
                           "Kraków": {"lat": 50.061683, "lon": 19.937348},
                           "Poznań": {"lat": 52.408493, "lon": 16.933593},
                           "Gdańsk": {"lat": 54.349658, "lon": 18.648023},
                           "Szczecin": {"lat": 53.432707, "lon": 14.548514},

                           "Łódź": {"lat": 51.759445, "lon": 19.457216},
                           "Lublin": {"lat": 51.246452, "lon": 22.568445},
                           "Katowice": {"lat": 50.264892, "lon": 19.023782},
                           "Białystok": {"lat": 53.132488, "lon": 23.168840},
                           "Bydgoszcz": {"lat": 53.123482, "lon": 18.008438},
                           "Olsztyn": {"lat": 53.778422, "lon": 20.480119},
                           "Rzeszów": {"lat": 50.041187, "lon": 21.999121},
                           "Toruń": {"lat": 53.013790, "lon": 18.598444},
                           "Opole": {"lat": 50.675015, "lon": 17.921297},
                           "Kielce": {"lat": 50.866077, "lon": 20.628567},
                           "Gorzów Wielkopolski": {"lat": 52.736819, "lon": 15.228507},
                           "Zielona Góra": {"lat": 51.935621, "lon": 15.506186}}


def get_distance_to_city_center(city, lat, lon):
    """
    Oblicza odległość w kilometrach między podanym punktem geograficznym a centrum podanego miasta.

    :param city: Nazwa miasta
    :param lat: Szerokość geograficzna punktu
    :param lon: Długość geograficzna punktu
    :return: Odległość w kilometrach
    """
    city_center = city_center_coordinates.get(city)
    if city_center is None or lat is None or lon is None:
        return None

    city_lat = city_center.get("lat")
    city_lon = city_center.get("lon")

    distance = haversine(lat, lon, city_lat, city_lon)
    return distance


def haversine(lat1, lon1, lat2, lon2):
    """
    Oblicza odległość w kilometrach między dwoma punktami geograficznymi na podstawie ich szerokości i długości geograficznej.

    :param lat1: Szerokość geograficzna pierwszego punktu
    :param lon1: Długość geograficzna pierwszego punktu
    :param lat2: Szerokość geograficzna drugiego punktu
    :param lon2: Długość geograficzna drugiego punktu
    :return: Odległość w kilometrach
    """
    R = 6371.0

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance


if __name__ == "__main__":
    point1 = (52.2296756, 21.0122287)  # Warszawa
    point2 = (41.8919300, 12.5113300)  # Rzym

    lat1, lon1 = point1
    lat2, lon2 = point2

    distance = haversine(lat1, lon1, lat2, lon2)
    print(f"Odległość między punktami wynosi: {distance:.2f} km")
