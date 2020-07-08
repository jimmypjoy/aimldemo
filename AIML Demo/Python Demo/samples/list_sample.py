
marks = [23,56,67]
marks.append(76)
marks.insert(2,60)
print(sum(marks))

print(max(marks))

print(len(marks))

print(min(marks))

print(60 in marks)
print("#####")
for mark in marks:
    print(mark)
print("#####")
animals = ['Cat', 'Dog','Elephant']
animals.append('Fish')
print(animals)
animals.pop()
print(animals)

squares_first_ten_numbers = [  i*i for i in range(1,11) ]
print(squares_first_ten_numbers)
print(type(squares_first_ten_numbers))

print("List comprehension#####")
print([len(str) for str in animals])
print([str for str in animals if len(str)>3])

print("List slice#####")
print(marks[0:2])
print(marks[0:])
print(marks[-2:])