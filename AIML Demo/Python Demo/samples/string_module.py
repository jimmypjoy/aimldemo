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

#prints below string 3 times
print(str1*3)

print('{} {} {}: {}'.format('my', 'name', 'is','Ji'))

str2 = input('Enter a text:')
print('You entered '+str2.upper())