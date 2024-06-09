import math

city_center_coordinates = {"Warszawa": {"lat": 52.231816, "lon": 21.006259},  # Pałac Kultury i Nauki
                           "Wrocław": {"lat": 51.108443, "lon": 17.040535},  # Galeria Dominikańska
                           "Kraków": {"lat": 50.061683, "lon": 19.937348},  # Sukiennice
                           "Poznań": {"lat": 52.408493, "lon": 16.933593},  # Studnia Bamberki
                           "Gdańsk": {"lat": 54.349658, "lon": 18.648023},  # Brama złota
                           "Szczecin": {"lat": 53.432707, "lon": 14.548514},  # Plac Grunwaldzki
                           "Łódź": {"lat": 51.761094, "lon": 19.463935},  # Kościół Najświętszego Imienia Jezus
                           "Lublin": {"lat": 51.248378, "lon": 22.559637},  # Plac Litewski
                           "Katowice": {"lat": 50.266107, "lon": 19.025328},  # Spodek Arena
                           "Białystok": {"lat": 53.132380, "lon": 23.158759},  # Ratusz na Rynku Kościuszki
                           "Bydgoszcz": {"lat": 53.122208, "lon": 17.999969},  # Zegar z czasem bydgoskim
                           "Olsztyn": {"lat": 53.777718, "lon": 20.474720},  # Zamek Kapituły Warmińskiej
                           "Rzeszów": {"lat": 50.037354, "lon": 22.004939},  # Pomnik Tadeusza Kościuszki
                           "Toruń": {"lat": 53.010504, "lon": 18.604116},  # Ratusz Staromiejski
                           "Opole": {"lat": 50.668627, "lon": 17.922295},  # Ratusz na rynku
                           "Kielce": {"lat": 50.869147, "lon": 20.627467},  # Pałac Biskupów Krakowskich
                           "Gorzów Wielkopolski": {"lat": 52.731107, "lon": 15.239115},  # Katedra na starym rynku
                           "Zielona Góra": {"lat": 51.938263, "lon": 15.505311}}  # Ratusz na starym rynku


def get_distance_to_city_center(city: str, lat: float, lon: float) -> float:
    """
    Calculate the distance between the city center and the given point.
    """
    city_center = city_center_coordinates.get(city)
    if city_center is None or lat is None or lon is None:
        return None

    city_lat = city_center.get("lat")
    city_lon = city_center.get("lon")

    distance = haversine(lat, lon, city_lat, city_lon)
    return distance


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points  on the earth (specified in decimal degrees)
    """

    R = 6371.0 # radius of the Earth
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
