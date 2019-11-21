a = "This is a string"
b = "this is another string"

# We can concatenate them together

c = a + ", and " + b

# We can split them apart
for w in a.split():
    print(w)

# We can change case
print(a.upper())
print(a.lower())

# we can test if a string contains another

if "is" in a:
    print("Yay!")
else:
    print("Boo!")
