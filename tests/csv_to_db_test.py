import unittest
from modules.csv_to_db import DataBase


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.db = DataBase("../data/first9000.db")

        self.austria = self.db.execute_selection_by_country("Austria")
        self.france = self.db.execute_selection_by_country("France")

    def test_locations_table(self):
        location_1 = "Europe, Austria, Ost, Industrieviertel, Wienerwald(IV), Thalhofergrat, ObereOstwand, ★★ Osterhasi"
        location_2 = "Europe, France, Île-de-France, Fontainebleau, Cuvier, BasCuvier, RedcircuitTD+(nº6), ★★★ La Marie Rose"

        self.assertEqual(self.austria[0].location, location_1)
        self.assertEqual(self.france[0].location, location_2)

    def test_difficulty(self):
        category_1 = "Intermediate"
        category_2 = "Experienced"

        self.assertEqual(self.austria[0].category, category_1)
        self.assertEqual(self.france[0].category, category_2)

    def test_style(self):
        style_1 = "Sport"
        style_2 = "Boulder"

        self.assertEqual(self.austria[0].style, style_1)
        self.assertEqual(self.france[0].style, style_2)


if __name__ == '__main__':
    unittest.main()
