
numbers=[1,2,3,4,5,1,2]
numbers_set=set(numbers)
print(numbers_set)

squares_first_ten_numbers_set = { i*i for i in range(1,11)}
print(squares_first_ten_numbers_set)
print(type(squares_first_ten_numbers_set))

#Example on how to use sets to do intersection , union and difference

l1 = [1,2,3,4,4]
l2 = [3,4,5,6]

s1 = set(l1)
s2 = set(l2)

print(s2 - s1) # difference  (whats in l2 and not in l1)
print(s1 - s2) # difference (whats in l1 and not in l2)
print(s2 | s1) # union
print(s2 & s1) # intersection