class LandAnimal:
    def walk(self):
        print('walk')

class WaterAnimal:
    def swim(self):
        print('swim')

class Amphibian(LandAnimal, WaterAnimal):
    pass

frog = Amphibian()

frog.swim()
frog.walk()

print(frog.__str__())

