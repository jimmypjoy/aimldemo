
tuple_var=(1,2,'test')
print(type(tuple_var))
print(tuple_var)
var1,var2,var3=tuple_var
print(var3)

tuple_var_list=list(tuple_var)
print(tuple_var_list)

for var in tuple_var:
    print(var)
