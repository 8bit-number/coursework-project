import os

from flask import Flask, render_template, request
from dotenv import load_dotenv

from modules.csv_to_db import DataBase
from modules.countries import locations
from modules.map_generator import get_mount_coords, get_shop_coords, create_map

app = Flask(__name__, template_folder="templates", static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

DIFFICULTIES = (
    "Beginner", "Intermediate", "Experienced", "Expert", "Elite"
)

db_path = ""
foursquare_client_id = ""
foursquare_client_secret = ""


@app.route("/", methods=['GET'])
def home():
    return render_template('main.html')


@app.route("/location", methods=['GET', 'POST'])
def location():
    countries = locations(db_path)

    kwargs = dict(
        ascents=None,
        countries=countries,
        difficulties=DIFFICULTIES
    )

    country = request.args.get('country')
    diff = request.args.get('difficulty')

    if not country and not diff:
        return render_template("location.html", **kwargs)

    db = DataBase(db_path)
    if diff != "":
        ascents = db.execute_selection_by_difficulty(country, diff)
    else:
        ascents = db.execute_selection_by_country(country)

    kwargs['ascents'] = ascents

    return render_template("location.html", **kwargs)


@app.route('/location/<int:route_id>')
def display_map(route_id):
    mountain_coordinates = get_mount_coords(route_id, db_path)
    shop_coordinates = get_shop_coords(
        mountain_coordinates,
        foursquare_client_id,
        foursquare_client_secret,
    )

    create_map(mountain_coordinates, shop_coordinates)

    return render_template("map.html")


if __name__ == '__main__':
    APP_ROOT = os.path.dirname(__file__)

    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)

    db_path = os.getenv("DB_PATH")
    foursquare_client_id = os.getenv("FOURSQUARE_CLIENT_ID")
    foursquare_client_secret = os.getenv("FOURSQUARE_CLIENT_SECRET")
    app.run(debug=True)
