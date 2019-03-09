# # >>> vector0 = Vector()
# #
# # >>> print(vector0)
# #
# # This is Vector(0, 0)
# #
# # >>> vector1 = Vector(1, 2)
# #
# # >>> print(vector1)
# #
# # This is Vector(1, 2)
# #
# # >>> vector2 = Vector(4, 8)
# # >>> vector0 = Vector()
# #
# # >>> print(vector0)
# #
# # This is Vector(0, 0)
# #
# # >>> vector1 = Vector(1, 2)
# #
# # >>> print(vector1)
# #
# # This is Vector(1, 2)
# #
# # >>> vector2 = Vector(4, 8)
# #
# # >>> print(vector2)
# #
# # This is Vector(4, 8)
# #
# # >>> vector = vector1.add(vector2)
# #
# # >>> print(vector)
# #
# # This is Vector(5, 10)
# #
# #
# # >>> print(vector2)
# #
# # This is Vector(4, 8)
# #
# # >>> vector = vector1.add(vector2)
# #
# # >>> print(vector)
# #
# # This is Vector(5, 10)
#
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "This is Vector({}, {})".format(self.x, self.y)

    def add(self, vector):
        # self.vecto
        return (self.x + vector.x, self.y + vector.y)
#
vector0 = Vector(1, 2)
vector1 = Vector(1,2)
print(vector0.add(vector1))
# class First:
#      def __init__(self, x, y):
#          self.x = 2 * x
#          self.y = self.x - y
#
#     def __str__(self):
#         return "First(" + str(self.x) + str(y) + ")"
#
#     def add_div(self, n):
#         return (self.x + n)/(self.y + 1)
#
#
#
# class Second(First):
#      def __init__(self, z, x, y):
#          self.x = x - y
#          self.y = x + y
#          self.z = 3 * z
#
#      def add_div(self):
#          return (self.x + self.z)/self.y
#
#
#
#
# def test():
#     try:
#         first, second = First(1, 2), Second(1, 3, 5)
#         print(first)
#         print(second)
#         print(first.add_div(4))
#         print(second.add_div())
#         print("Finish!")
#
#     except:
#         print("Stop!")
#
#
#
#
# test()
