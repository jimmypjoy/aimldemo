import module_1 as m1

print('inside module2....')
print(m1.name1)
m1.method_1()
m1.ClassA().class_method_1()

#check teh contents of module m1
print(dir(m1))