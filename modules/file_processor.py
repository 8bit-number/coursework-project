class Processor:

    def process(self, row):
        """
        Method for processing the .csv file
        :return:
        """
        full_location = ', '.join(self.merge_columns(row))
        country, style, diff, category = row[0], row[-3], row[-2], row[-1]
        return Ascent(country, full_location, style, diff,
                      category).get_data()

    def merge_columns(self, row):
        """
        Method for merging several columns into one mutual one
        :param row:
        :return:
        """
        options = ["Unknown", "Sport", "Trad", "Boulder", "Ice", "Mixed"]
        for i in range(len(row)):
            if row[i] in options:
                return row[0:i]


class Ascent:
    def __init__(self, country, location, style, grade, sign):
        self.country = country
        self.location = location
        self.style = style
        self.grade = grade
        self.sign = sign

    @property
    def category(self):
        if self.sign == 'gb1':
            return "Beginner"
        elif self.sign == "gb2":
            return "Intermediate"
        elif self.sign == "gb3":
            return "Experienced"
        elif self.sign == "gb4":
            return "Expert"
        elif self.sign == "gb5":
            return "Elite"
        else:
            return 'n/a'

    def get_data(self):
        return self.country, self.location, self.style, self.grade, self.category


if __name__ == "__main__":
    import csv

    file1 = Processor()
    with open("test.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            file1.process(row)
            break
