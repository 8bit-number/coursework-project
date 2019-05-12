import unittest
from modules.transfer_file_to_db import DataBase


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.db = DataBase("../data/testing.db")

        self.austria = self.db.execute_selection_by_country("Austria")
        self.france = self.db.execute_selection_by_country("France")

        self.

    def test_locations_table(self):
        location_1 = "Europe, Austria, West, Rheintal, Känzele(Bregenz), Traumland, Dornröschen"
        location_2 = "Europe, France, Auvergne-Rhône-Alpes, Auvergne, Puy-de-Dôme, Lamontagnepercée, ★★ Aerial"

        self.assertEqual(self.austria[0].location, location_1)
        self.assertEqual(self.france[0].location, location_2)

    def test_difficulty(self):
        category_1 = "Intermediate"
        category_2 = "Intermediate"

        self.assertEqual(self.austria[0].category, category_1)
        self.assertEqual(self.france[0].category, category_2)

    def test_


if __name__ == '__main__':
    unittest.main()
