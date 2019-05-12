from flask import Flask, render_template, url_for, request
from modules.csv_to_db import DataBase
from modules.countries_db import countries
from modules.map_generator import *

app = Flask(__name__, template_folder="../templates",
            static_folder='../static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

difficulties = ["Beginner", "Intermediate", "Experienced", "Expert",
                "Elite"]


@app.route("/", methods=['GET', 'POST'])
def home():
    # return render_template("home_hugo.html")

    if request.method == "GET" and not request.args.get('country'):
        return render_template('home.html', locations=countries,
                               difficulties=difficulties)
    else:
        country = request.args.get('country')
        diff = request.args.get("difficulty")
        db = DataBase(
            "/home/nastya/PycharmProjects/course_work/data/locations.db")
        if diff != "None":
            all_data = db.execute_selection_by_difficulty(country,
                                                          diff)
        else:
            all_data = db.execute_selection_by_country(country)
        return render_template("table.html", ascents=all_data)


@app.route('/location/<int:route_id>')
def display_map(route_id):
    mountain_coordinates = get_mount_coords(route_id)
    shop_coordinates = get_shop_coords(mountain_coordinates)
    create_map(mountain_coordinates, shop_coordinates)
    return render_template("map.html")


if __name__ == '__main__':
    app.run(debug=True)
