from functools import reduce

def multiply_by_2(data):
    """ sample function to multiply by 22 to be used as a lamda example"""
    return data*2
def do_this_and_print(func,num):
    print(func.__doc__)
    print(func(num))

print(multiply_by_2.__doc__)

do_this_and_print(multiply_by_2,125)

do_this_and_print(lambda data:data*3, 200)

numbers= [1,7,24,23,14]
print(list(filter(lambda x:x%7==0,numbers)))
print(numbers)

fun_lamda = lambda x:print(x)
fun_lamda(2)
fun_lamda('testprint')

words = ["Apple", "Ant", "Bat"]
print(list(filter(lambda x: x.endswith('at'), words)))
print(list(map(lambda x: x.upper(), words)))
print(list(map(lambda x: x*2, numbers)))
print(reduce(lambda x,y:x+y ,numbers))
print(reduce(lambda x,y:max(x,y) ,numbers ))