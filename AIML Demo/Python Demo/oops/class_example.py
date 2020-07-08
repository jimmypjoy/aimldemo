# MotorBike
 # gear, speed
from builtins import print


class Book:

    def __init__(self, name, copies):
        print('inside __init__')
        self.name = name
        self.copies = copies

    def __repr__(self):
        return repr((self.name, self.copies))

    def increase_copies(self, how_much):
        self.copies += how_much

    def decrease_copies(self, how_much):
        self.copies -= how_much

    def test_method(self):
        print('##### inside test method####')


book1 = Book('Mastering Spring 5.0', 200)
book1.increase_copies(50)

book2 = Book('Mastering Python 3', 15)
book2.decrease_copies(5)

book2.test_method()

print(book1)
print(book2)
