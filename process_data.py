import json, requests
import folium
import sqlite3


def get_mount_coords(asc_id):
    with sqlite3.connect("myTable2.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT coordinates FROM locations WHERE id in (?)",
            (asc_id,))
        return cursor.fetchone()[0]


def get_shop_coords(mountain_coords):
    url = 'https://api.foursquare.com/v2/venues/search'

    params = dict(
        client_id="Y0VAAR4NLGYIAGUR0RNOE14XPTLKGG3FYGBYWMIBX4YGCDQL",
        client_secret="3JOSMX2UEJNK4PVDANRW4OWUOKWO5TZS3VLRGXC4NWN4RIZH",
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

    map1.save("templates/map.html")

    # return "map.html"

# mountain_coordinates = get_mount_coords(68)
# shop_coordinates = get_shop_coords(mountain_coordinates)
# fname = create_map(mountain_coordinates, shop_coordinates)
# print(fname)
