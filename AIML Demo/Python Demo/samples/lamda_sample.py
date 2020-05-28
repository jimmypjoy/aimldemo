from functools import reduce

def multiply_by_2(data):
    return data*2
def do_this_and_print(func,num):
    print(func(num))

do_this_and_print(multiply_by_2,125)

do_this_and_print(lambda data:data*3, 200)

numbers= [1,7,24,23,14]
print(list(filter(lambda x:x%7==0,numbers)))
print(numbers)

words = ["Apple", "Ant", "Bat"]
print(list(filter(lambda x: x.endswith('at'), words)))
print(list(map(lambda x: x.upper(), words)))
print(list(map(lambda x: x*2, numbers)))
print(reduce(lambda x,y:x+y ,numbers))
print(reduce(lambda x,y:max(x,y) ,numbers ))