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


@app.route("/", methods=['GET', 'POST'])
def home():
    countries = locations(db_path)

    if request.method == "GET" and not request.args.get('country'):
        return render_template(
            'main.html', locations=countries, difficulties=DIFFICULTIES,
        )

    country = request.args.get('country')
    diff = request.args.get("difficulty", None)

    db = DataBase(db_path)
    if diff != "None":
        all_data = db.execute_selection_by_difficulty(country, diff)
    else:
        all_data = db.execute_selection_by_country(country)

    return render_template("table.html", ascents=all_data)


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
