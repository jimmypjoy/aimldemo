import string

print(string.digits)
print(string.ascii_letters)
print(string.ascii_uppercase)
print(string.punctuation)
for str in string.ascii_uppercase:
    print(str)

str1='test_string'
print(str1.lower())
print(str1.upper())

print(str1.split('_'))

str2='''line 1
line 2 \"testquote\"
line 3'''
print(str2)
print('Length of string:{}'.format(len(str1)))
print('Print charcter at index x:{}'.format(str1[0]))
print('Print slice of string:{}'.format(str1[0:2]))

#prints below string 3 times
print(str1*3)

print('{} {} {}: {}'.format('my', 'name', 'is','Ji'))

str2 = input('Enter a text:')
print('You entered '+str2.upper())

a = "Hello, World!"
print(a[1])

txt = "My name is John, and I am {}"
txt1=txt.format(36)
print(txt1)

myorder = "I have a {carname}, it is a {model}."
print(myorder.format(carname = "Ford", model = "Mustang"))