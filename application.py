from flask import Flask, render_template, url_for, request
from transfer_file_to_db import *
from countries_db import countries
from process_data import *

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

difficulties = ["Beginner", "Intermediate", "Experienced", "Expert",
                "Elite"]


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "GET" and not request.args.get('country'):
        return render_template('home.html', locations=countries,
                               difficulties=difficulties)
    else:
        country = request.args.get('country')
        diff = request.args.get("difficulty")
        db = DataBase("myTable2.db")
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


# if user doesnt know their level, write

if __name__ == '__main__':
    app.run(debug=True)
