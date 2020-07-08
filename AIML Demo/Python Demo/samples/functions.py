def print_message(text):
    """Test function"""
    global global_variable
    global_variable=7
    print('You passed {} ....'.format(text))

print_message('test')

print(global_variable)

print(print_message.__doc__)

def fun2(first_name,last_name):
    print('My first name is {} and last name is {}'.format(first_name,last_name))

fun2('jim', 'jo')
fun2(last_name='jo', first_name='j')

def fun3(str1):
    return str1.upper()

print(fun3('test'))