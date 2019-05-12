import sqlite3

with sqlite3.connect(
        "/home/nastya/PycharmProjects/course_work/data/locations.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT location FROM locations")
    countries = [i[0] for i in cursor.fetchall()]
