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