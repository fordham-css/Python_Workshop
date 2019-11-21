# This will show you the basic flow control in python
# It really isn't a whole lot different from most languages

# Also see how easily you can concatenate strings
print("Unlike some languages, python has no main function, it just runs anything in your "
      "python file")
condition = True
if condition:
    print("If statements are pretty easy to deal with")
else:
    print("Just don't forget the colons and indent")

def aFunction():
    '''This is how you define a function.  I'll do more about functions later.'''
    print("That string above is called a DOCSTRING")

print("Functions won't run until they're called")
aFunction()
print(aFunction.__doc__)

a_list = [1, 5, 7, 9, 2, 8]

for num in a_list:
    if num == 7:
        break
    print(num)

b = 5

while(b > 0):
    b = b - 1

for i in range(9):
    print(i)