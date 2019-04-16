import csv


class Processor:
    def __init__(self, filename):
        self.file = filename
        # self.content = self.process()

    def process(self):
        """
        Method for processing
        :return:
        """
        with open(self.file) as f:
            reader = csv.reader(f)
            for row in reader:
                new_row = ', '.join(self.merge_columns(row))
                print(new_row)
                # new_row = [' '.join([row[0], row[1]])]
                # print(row)
                # print(Ascent(row[0], None, row[-3], row[-2], row[-1]))

    # Australia, Victoria, MelbourneandSurrounds, InnerMelbourne, BurnleyBoulderingWall, Wall1 - Verticalwall, Boulder, Unknown, Unknown

    def merge_columns(self, row):

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

    def __str__(self):
        return "The ascent, located in {} is {} styled-wall, its grade is: {}, category: {}".format(
            self.country, self.style, self.grade, self.category)

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


file1 = Processor("test.csv")
# file1.process()

file1.merge_columns(
    ['Australia', 'Victoria', 'NorthWest', 'Arapiles', 'BushrangerBluff',
     'MainWall', 'Trad', '14', 'gb2'])
file1.merge_columns(
    ['Australia', 'Victoria', 'NorthWest', 'Arapiles', 'NAME', 'MainWall',
     'Unknown', 'Unknown', 'gb2'])
