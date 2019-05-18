import json, requests
import folium
import sqlite3


def get_mount_coords(asc_id, db_path):
    """
    Function for getting the latitude and longitude of the climbing route
    by making a request to database
    :param asc_id: int - identification of the ascent
    :param db_path: str - relative path to database
    :return:
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT coordinates, location FROM locations WHERE id in (?)",
            (asc_id,))
        rez = cursor.fetchall()
        coordinates = rez[0][0]
        route_name = rez[0][1]
        return coordinates, route_name


def get_shop_coords(mountain_coords, client_id, client_secret):
    """
    Sends a request to Foursquare API, in order to get the coordinates
    of shops, where it is possible to buy sports equipment
    :param mountain_coords: str - (lat, lon)
    :param client_id: str - client id, provided by Foursquare API
    :param client_secret: str - client secret, provided by Foursquare API
    :return: dict - {name of the shop: (latitude, longitude)}
    """
    url = 'https://api.foursquare.com/v2/venues/search'

    params = dict(
        client_id=client_id,
        client_secret=client_secret,
        v='20180420',
        ll=mountain_coords,
        intent='browse',
        radius="50000",
        categoryId="4bf58dd8d48988d1f1941735"
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    resp = dict()
    for i in data["response"]["venues"]:
        resp[i["name"]] = (i["location"]["lat"], i["location"]["lng"])

    return resp


def create_map(mountain_coords, shop_coords, route_name):
    """
    Function for creating a folium map
    :param mountain_coords: str - (lat, lon)
    :param shop_coords: str - (lat, lon)
    :param route_name: str - name of the route, that is used to make
    folium map look more user-friendly
    :return:
    """
    s = list(map(float, mountain_coords.strip().split(",")))
    map1 = folium.Map(location=[s[0], s[1]])
    folium.Marker([s[0], s[1]], popup=route_name).add_to(
        map1)

    for i in shop_coords:
        folium.Marker([shop_coords[i][0], shop_coords[i][1]],
                      popup=str(i),
                      icon=folium.Icon(color='blue')).add_to(map1)

    return map1._repr_html_()


if __name__ == "__main__":
    from modules.config import path_to_map, path_to_db, client_secret, \
        client_id

    mounts = get_mount_coords(1, path_to_db)
    shops = get_shop_coords(mounts[0], client_id, client_secret)
    create_map(mounts[0], shops, "route1")
