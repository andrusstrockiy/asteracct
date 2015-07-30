#!/usr/bin/env python
# encoding: utf8
# -*- coding: KOI8-*-
__author__ = 'andruss'

# An example of a class
class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.description = "This shape has not been described yet"
        self.author = "Nobody has claimed to make this shape yet"

    def area(self):
        return self.x * self.y

    def perimeter(self):
        return 2 * self.x + 2 * self.y

    def describe(self, text):
        self.description = text

    def authorName(self, text):
        self.author = text

    def scaleSize(self, scale):
        self.x = self.x * scale
        self.y = self.y * scale


# The shape looks like this:
# _________
#|    |    |
#|    |    |
#|____|____|

class Square(Shape):
    def __init__(self, x):
        self.x = x
        self.y = x


class DoubleSquare(Square):
    def __init__(self, y):
        self.x = 2 * y
        self.y = y

    def perimeter(self):
        return 2 * self.x + 3 * self.y




sqr = Square(50)

print(sqr.area())
print(sqr.author)
dsqr = DoubleSquare(15)


print(dsqr.perimeter())

#
# rectangle = Shape(100, 45)
# print('Area:' + str(rectangle.area()))
#
# #finding the perimeter of your rectangle:
# print rectangle.perimeter()
#
# print(rectangle.description)
# #describing the rectangle
# rectangle.describe("A wide rectangle, more than twice as wide as it is tall")
# print('After')
# print(rectangle.description)
#
# #making the rectangle 50% smaller
# rectangle.scaleSize(0.5)
#
# #re-printing the new area of the rectangle
# print rectangle.area()
