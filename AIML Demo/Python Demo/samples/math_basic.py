import math

print(help(math))
value = 4.35
print(math.floor(value))
print(math.ceil(value))
print(round(value))
print(math.pi)
print(math.e)
print(math.log(math.e))
print(math.log(10))
print(math.sin(10))
print(math.radians(180))



def print_squares_of_numbers_upto(n):
    for i in range(1,n+1):
        print(i*i)


def print_squares_of_even_numbers_upto(n):
    for i in range(2,n+1,2):
        print(i*i)


def sum_of_two_numbers(number1,number2):
    sum = number1 + number2
    return sum


def print_numbers_in_reverse(n):
    for i in range(n,0,-1):
        print(i)

print("print(sum_of_two_numbers(5,6))")
print(sum_of_two_numbers(5,6))
print("print_squares_of_even_numbers_upto(10)")
print_squares_of_even_numbers_upto(10)
print("print_numbers_in_reverse(10)")
print_numbers_in_reverse(10)
print("print_squares_of_numbers_upto(4)")
print_squares_of_numbers_upto(4)