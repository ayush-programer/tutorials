# Python3 Input Example

name = input("Type in your name: ")
print("Hello, " + name + "!")

age = input("Type in your age: ")
age = int(age)

if age >= 18:
    print("You've grown up!")
else:
    print("You're still a child!")

# Note: In Python2, input() interprets
# user's input as code and attempts to
# run it; use raw_input() instead

print("Type in a grocery (or q to quit): ")

grocery_list = []
user_input = ""

while user_input != "q":
    user_input = input()

    if user_input != "q":
        grocery_list.append(user_input)

print("You will need to buy:")

while grocery_list:
    current_grocery = grocery_list.pop()
    print("\t* " + current_grocery)

# Note: You can use 'break' and 'continue'
# like in C/C++ (and similar)
