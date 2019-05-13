import json, requests
import folium
import sqlite3


def get_mount_coords(asc_id, db_path):
    """
    function for getting the latitude and longitude
    :param asc_id:
    :return:
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT coordinates FROM locations WHERE id in (?)",
            (asc_id,))
        return cursor.fetchone()[0]


def get_shop_coords(mountain_coords, client_id, client_secret):
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


def create_map(mountain_coords, shop_coords):
    """
    Function for creating folium map
    :param mountain_coords: string
    :param shop_coords: string
    :return: None
    """
    s = list(map(float, mountain_coords.strip().split(",")))
    map1 = folium.Map(location=[s[0], s[1]])
    folium.Marker([s[0], s[1]], popup="name of the ascent").add_to(
        map1)

    for i in shop_coords:
        folium.Marker([shop_coords[i][0], shop_coords[i][1]],
                      popup=str(i),
                      icon=folium.Icon(color='blue')).add_to(map1)

    map1.save(
        "/home/nastya/PycharmProjects/course_work/templates/map.html")

    return "/home/nastya/PycharmProjects/course_work/templates/map.html"
