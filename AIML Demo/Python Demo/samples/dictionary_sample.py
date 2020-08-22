occurances = dict(a=5, b=6, c=8, e=9)
print(occurances)
print(occurances.get('b'))
del (occurances['e'])

for key in occurances.keys():
    print(occurances.get(key) ** 2)

print(len(occurances))
print(6 in occurances.values())
print('b' in occurances.keys())

for key, value in occurances.items():
    print(key + '---' + str(value))
    print('{}&&&:{}'.format(key, value))

squares_first_ten_numbers_set = {i: i * i for i in range(1, 11)}
print(squares_first_ten_numbers_set)
print(type(squares_first_ten_numbers_set))
