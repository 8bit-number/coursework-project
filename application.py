from flask import Flask, render_template, request

from modules.csv_to_db import DataBase
from modules.countries import locations
from modules.map_generator import get_mount_coords, get_shop_coords, \
    create_map
from modules.config import client_id, client_secret, path_to_db, \
    path_to_map

app = Flask(__name__, template_folder="templates",
            static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

DIFFICULTIES = (
    "Beginner", "Intermediate", "Experienced", "Expert", "Elite"
)


@app.route("/", methods=['GET'])
def home():
    return render_template('main.html')


@app.route("/location", methods=['GET', 'POST'])
def location():
    countries = locations(path_to_db)

    kwargs = dict(
        ascents=None,
        countries=countries,
        difficulties=DIFFICULTIES
    )

    country = request.args.get('country')
    diff = request.args.get('difficulty')

    if not country and not diff:
        return render_template("location.html", **kwargs)

    db = DataBase(path_to_db)
    if diff != "":
        ascents = db.execute_selection_by_difficulty(country, diff)
    else:
        ascents = db.execute_selection_by_country(country)

    kwargs['ascents'] = ascents

    return render_template("location.html", **kwargs)


@app.route('/location/<int:route_id>')
def display_map(route_id):
    mountain_coordinates = get_mount_coords(route_id, path_to_db)
    shop_coordinates = get_shop_coords(
        mountain_coordinates, client_id, client_secret)

    location_map = create_map(mountain_coordinates, shop_coordinates, path_to_map)

    return render_template("map.html", location_map=location_map)


if __name__ == '__main__':
    app.run(debug=True)

# "/home/nastya/PycharmProjects/course_work/templates/map.html"
