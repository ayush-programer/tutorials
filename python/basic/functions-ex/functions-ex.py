# Python3 Fuction Examples

import module_ex

module_ex.greet_from_module()
# Hello from module!

from module_ex2 import add_numbers

print(add_numbers(5, 6))
# 11

from module_ex2 import another_greeting as greet

greet()
# Hello from another module!

# Note: To import all functions from a module
# use e.g. from module_ex import *

def hello(user="root", age=100):
    hello_string = "Hello, " + user
    hello_string += "! I hear your age is " + str(age) + "."
    print(hello_string)

# positional arguments
hello("Stjepan", 34)
# Hello, Stjepan! I hear your age is 34.

# keyword arguments
hello(age=34, user="Stjepan")
# Hello, Stjepan! I hear your age is 34.

test = hello()
# Hello, root! I hear your age is 100.

print(test)
# None

def get_hello_string(name, surname=""):
    hello_string = "Hello, " + name + "!"
    return hello_string

message = get_hello_string("Stjepan")
print(message)
# Hello, Stjepan!

def append_to_list(list):
    list.append(9000)

test_list = [ 1, 2, 3 ]
append_to_list(test_list)
print(test_list)
# [1, 2, 3, 9000]

test_list.remove(9000)
print(test_list)
# [1, 2, 3]

append_to_list(test_list[:])
print(test_list)
# [1, 2, 3]

# Note: The slice notation [:] will
# send a copy of the list to the
# function

# variable number of arguments

def append_elements_to_list(list, *elements):
    list.extend([element for element in elements])

append_elements_to_list(test_list, 4, 5, 6)
print(test_list)
# [1, 2, 3, 4, 5, 6]

# function decorator syntax

def append_element_to_list_f(f):
    def wrapper(list, el):
        list.append(f(el))
        return list
    return wrapper

@append_element_to_list_f
def append_squared(el):
    return el * el

print(append_squared([1,2,3], 5))
