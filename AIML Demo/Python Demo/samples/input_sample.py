print('Enters a string:')
str1= input()
print('You entered:{}'.format(str1))

print('Enters a Number:')
try:
    int1= int(input())
    print('You entered:{}'.format(int1))
except:
    print('Value is not a number')
