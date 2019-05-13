import sqlite3


def locations(db_path):
    res = []
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT location FROM locations")
        res = [i[0] for i in cursor.fetchall()]

    return res
