import csv
import sqlite3
from modules.ascent_processor import Ascent


class DataBase:
    """ Class, that represents the database """

    def __init__(self, db_name):
        self.db_name = db_name

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(""" CREATE table locations (
                    id int,
                    location text,
                    name text,
                    style text,
                    difficulty text,
                    category text,
                    coordinates text
                    )""")
        print("table created successfully!")
        conn.commit()

    def merge_columns(self, row):
        """
        method to get full name of ascent as a string
        :param row: string
        :return: string
        """
        options = ["Unknown", "Sport", "Trad", "Boulder", "Ice",
                   "Mixed",
                   "Aid", "Top rope", "Traverse", "Deep water solo",
                   None,
                   "Via ferrata", "Alpine"]
        for i in range(len(row)):
            if row[i] in options:
                return row[0:i]

    @staticmethod
    def page_increment(num):
        num += 1
        return num

    def insert_to_table(self):
        """
        Method for inserting data into table
        :return:
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            with open("../data/data.csv") as f:
                reader = csv.reader(f)
                i = 1
                for row in reader:
                    ascent_row = Ascent(i, row[1],
                                        ', '.join(
                                            self.merge_columns(row)),
                                        coords=row[-1], style=row[-4],
                                        grade=row[-3],
                                        sign=row[-2])
                    processed = ascent_row
                    cursor.execute(
                        'INSERT INTO locations VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (i, processed.country, processed.location,
                         processed.style, processed.grade,
                         processed.category, processed.coords))
                    i += 1
        print("inserted to db successfully!")
        conn.commit()

    def execute_selection_by_country(self, country):
        """
        Method for getting all the mountains and ascents of the certain country,
        that is being chosen by user.
        :param country: str: name of the country
        :return: cursor object: object, that is needed for future work with db connection
        """

        query = "SELECT * FROM locations where location in (?) and category NOT in (?)"

        rez = []
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            selection = cursor.execute(query, (country, "n/a"))
            for tup in selection:
                rez.append(Ascent(my_id=tup[0], country=tup[1],
                                  coords=tup[-1],
                                  location=tup[2],
                                  style=tup[3],
                                  grade=tup[4], sign=None,
                                  category=tup[5]))

        return rez

    def execute_selection_by_difficulty(self, country, diff):
        query = "SELECT * FROM locations where location in (?) AND category in (?)"
        rez = []
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            selection = cursor.execute(query, (country, diff))
            # print(selection.fetchall())
            for tup in selection:
                # print(tup)
                rez.append(
                    Ascent(my_id=tup[0],
                           country=tup[1], coords=tup[-1],
                           location=tup[2],
                           style=tup[3],
                           grade=tup[4], sign=None,
                           category=tup[5]))

        return rez

    def get_all_countries(self):
        # rez = []
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT location FROM locations")
            countries = [i[0] for i in cursor.fetchall()]
        return countries


d = DataBase("../data/routes.db")
# print(d.get_all_countries())
# d.create_table()
# d.insert_to_table()

# print(d.get_all_countries())
# selected = d.execute_selection_by_country("Austria")[0]
# selected_2 = d.execute_selection_by_country("France")[0]
# print(selected.style)
# print(selected_2.style)
# for i in selected[0:2]:
#     print(i.category)
# d.create_table()
# d.insert_to_table()
# print([0].location)
# print(d.execute_selection_by_difficulty("Austria", "Experienced"))
