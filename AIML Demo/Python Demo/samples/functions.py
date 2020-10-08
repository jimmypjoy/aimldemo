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

def test_var_args(f_arg, *argv):
    print("first normal arg:", f_arg)
    for arg in argv:
        print("another arg through *argv:", arg)

test_var_args('var1', 'python', 'var2', 'var3')

def greet_me(**kwargs):
    for key, value in kwargs.items():
        print("{0} = {1}".format(key, value))

greet_me(name="n1",name2="n2")

#*args
def myfunc(*args):
    return sum(args)*.05
print(myfunc(40,60,20))

#**kwargs
def myfunc(**kwargs):
    if 'fruit' in kwargs:
        print(
            f"My favorite fruit is {kwargs['fruit']}")  # review String Formatting and f-strings if this syntax is unfamiliar
    else:
        print("I don't like fruit")

myfunc(fruit='pineapple')