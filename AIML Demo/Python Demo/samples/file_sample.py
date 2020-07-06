file=open('C:/gitworkspace/aimldemo/AIML Demo/Python Demo/inputs/sample_input.txt')
print(file.read())
print(file.closed)
file.close()
print(file.closed)

with open('C:/gitworkspace/aimldemo/AIML Demo/Python Demo/inputs/sample_input.txt') as the_file:
    for line in the_file:
        print(line.rstrip())

with open('C:/gitworkspace/aimldemo/AIML Demo/Python Demo/inputs/sample_input.txt','a') as the_file:
    the_file.write('\n')
    the_file.write('New line from program')