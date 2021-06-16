import random
import time

from pymongo import MongoClient

# Init
client = MongoClient('localhost', 27017)
db = client['citeos']
collection_villes = db['villes']
collection_routes = db['routes']
collection_depots = db['depots']


def generate_cities(n):
    collection_villes.drop()
    collection_routes.drop()

    cities = []
    roads = []

    start = time.perf_counter()

    for i in range(1, n + 1):
        cities.append({"id_ville": i})
        for j in range(i - 1, -1, -1):
            if random.random() > 0.95:
                roads.append({"route": "route " + str(i) + "/" + str(j),
                              "id_ville_1": i,
                              "id_ville_2": j,
                              "est_oriente": True,
                              "poids_1": int(random.random() * 590 + 10),
                              "poids_2": int(random.random() * 590 + 10),
                              "trafic": [random.random() * 0.50 + 0.50 for _ in range(0, 24, 4)]
                              })
            else:
                roads.append({"route": "route " + str(i) + "/" + str(j),
                              "id_ville_1": i,
                              "id_ville_2": j,
                              "est_oriente": False,
                              "poids": int(random.random() * 590 + 10),
                              "trafic": [random.random() * 0.50 + 0.50 for _ in range(0, 24, 4)]
                              })
        if len(roads) >= 1000:
            collection_routes.insert_many(roads)
            roads = []
    collection_villes.insert_many(cities)
    if roads: collection_routes.insert_many(roads)
    print(time.perf_counter() - start)


generate_cities(1000)
