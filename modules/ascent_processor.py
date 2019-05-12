class Ascent:
    def __init__(self, my_id, country, location, coords, style, grade,
                 sign=None,
                 category='n/a'):

        self.country = country
        self.location = location
        self.style = style
        self.grade = grade
        if sign:
            self.sign = sign
            self.category = category

        if category is not "n/a":
            self._category = category
        self.sign = sign
        self.category = category

        self.coords = coords
        self.my_id = my_id

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):

        if self.sign == 'gb1':
            self._category = "Beginner"
        elif self.sign == "gb2":
            self._category = "Intermediate"
        elif self.sign == "gb3":
            self._category = "Experienced"
        elif self.sign == "gb4":
            self._category = "Expert"
        elif self.sign == "gb5":
            self._category = "Elite"
        else:
            self._category = category

    def get_data(self):
        return self

    # def __str__(self):
    #     return f"country is {self.country} \n" \
    #         f"full name is {self.location} \n" \
    #         f"style is {self.style} \n" \
    #         f"grade is {self.grade} \n" \
    #         f"category is {self.category} \n" \
    #         f"coord is {self.coords} \n"

    def __repr__(self):
        return f"({self.location}, {self.style}, {self.grade}, {self.category})"
