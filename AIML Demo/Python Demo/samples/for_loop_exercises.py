marks = [23, 24,56,67]
for mark in marks:
    if mark==67:
        break
    if mark==56:
        continue
    print(mark)

# print range in the increment of 3
for i in range(0,10,3):
    print(i)


def is_prime(number):

    if number < 2:
        return False

    for divisor in range(2,number):
        if number % divisor == 0:
            return False

    return True

# print(is_prime(15));


def sum_upto_n(number):

    sum = 0

    for i in range(1, number+1):
        sum = sum + i

    return sum


# print(sum_upto_n(6))
# print(sum_upto_n(10))


def calculate_sum_of_divisors(number):
    sum_of_divisors = 0

    for divisor in range(1,number+1):
        if number % divisor == 0:
            sum_of_divisors = sum_of_divisors + divisor

    return sum_of_divisors

# print(calculate_sum_of_divisors(6))
# print(calculate_sum_of_divisors(15))


def print_a_number_triangle(number):
    for j in range(1, number + 1):
        for i in range(1, j + 1):
            print(i, end=' ')
        print()


print_a_number_triangle(6)
print(is_prime(19))
print(sum_upto_n(19))
print('##########enumerate')
numbers1 = [1,4,6,3,4]
for index,number in enumerate(numbers1):
    print(f'{index} - {number}')