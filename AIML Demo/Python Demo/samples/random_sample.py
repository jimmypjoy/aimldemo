import random

print(random.randint(0,100))
print(random.randint(0,100))

mylist = list(range(0,20))
print(random.choice(mylist))
random.shuffle(mylist)
print(mylist)