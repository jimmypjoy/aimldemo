def method_1():
    print("method 1 inside module 1")

print('print from module 1- non method')

class ClassA:
    def class_method_1(self):
        print("ClassA.class_method_1 from  ClassA.method 1 inside module 1")

# print(__name__)
name1='name1text'

if __name__ == '__main__':
    print('print from module 1- non method-only for main')
    method_1()
    ClassA().class_method_1()
    print('Executed when invoked directly')
else:
    print ('Executed when imported')