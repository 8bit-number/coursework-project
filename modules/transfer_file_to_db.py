import sqlite3
import csv
from modules.file_processor import Processor

conn = sqlite3.connect("locations_of_ascents.db")
c = conn.cursor()

# code for creating the table
# c.execute(""" CREATE table locations (
#         location text,
#         name text,
#         style text,
#         difficulty text,
#         category text
#         )""")


file1 = Processor()
with open("test.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        processed = file1.process(row)
        c.execute('INSERT INTO locations VALUES (?, ?, ?, ?, ?)', processed)

c.execute("SELECT * FROM locations where category in ('Beginner')")

print(c.fetchall())

conn.commit()
conn.close()
