# Python3 List Examples

empty_list = []

print(empty_list)
# []

if empty_list:
    print("List is not empty")
else:
    print("List is empty")
# List is empty

fruit = ["banana", "pineapple", "apple", "cherry"]

print(fruit)
# ['banana', 'pineapple', 'apple', 'cherry']

print(fruit[0] + " and " + fruit[2])
# banana and apple

print(fruit[-1] + " and " + fruit[-3])
# cherry and pineapple

fruit.append("tomato")
print(fruit)
# ['banana', 'pineapple', 'apple', 'cherry', 'tomato']

del fruit[-1]               # remove by position
fruit.remove("pineapple")   # remove by value
print(fruit)
# ['banana', 'apple', 'cherry']

fruit.insert(1, "pineapple")
print(fruit)
# ['banana', 'pineapple', 'apple', 'cherry']

last_fruit = fruit.pop()
print(last_fruit)
# cherry

second_fruit = fruit.pop(1)
print(second_fruit)
# pineapple

vegetables = ['spinach', 'tomato', 'cucumber']

vegetables.reverse()
print(vegetables)
# ['cucumber', 'tomato', 'spinach']

print(sorted(vegetables))
# ['cucumber', 'spinach', 'tomato']

print(vegetables)
# ['cucumber', 'tomato', 'spinach']

vegetables.sort()
print(vegetables)
# ['cucumber', 'spinach', 'tomato']

animals = ['dog', 'cat', 'mouse']

animals.sort(reverse=True)
print(animals)
# ['mouse', 'dog', 'cat']

print(len(animals))
# 3

print("Animal list:")
for animal in animals:
    print("\t* " + animal)
# Animal list:
#       * mouse
#       * dog
#       * cat

print(list(range(1, 5)))
# [1, 2, 3, 4]

print("First three numbers:")
for value in range(1, 4):
    print("\t* " + str(value))
# First three numbers:
#       * 1
#       * 2
#       * 3

odd_numbers = list(range(11, 21, 2))
print("Odd numbers in [10, 20]: " + str(odd_numbers))
# Odd numbers in [10, 20]: [11, 13, 15, 17, 19]

print(min(odd_numbers))
# 11

print(max(odd_numbers))
# 19

print(sum(odd_numbers))
# 75

# list comprehension

triple_even_numbers = [3 * value for value in range(1,11,2)]
print(triple_even_numbers)
# [3, 9, 15, 21, 27]

# slicing a list

print(triple_even_numbers[1:4])
# [9, 15, 21]

print(triple_even_numbers[:3])
# [3, 9, 15]

# Note: This is the same as
# triple_even_numbers[0:3]
# triple_even_numbers[:-2]

print(triple_even_numbers[3:])
# [21, 27]

# Note: This is the same as
# triple_even_numbers[3:len(triple_even_numbers)]
# triple_even_numbers[-2:]

print("Some numbers:")
for number in triple_even_numbers[2:4]:
    print("\t* " + str(number))
# Some numbers:
#       * 15
#       * 21

triple_even_numbers_copy = triple_even_numbers[:]

del triple_even_numbers_copy[0]
del triple_even_numbers[-1]

print(triple_even_numbers_copy)
# [9, 15, 21, 27]

print(triple_even_numbers)
# [3, 9, 15, 21]

print(", ".join(["a", "b", "c"]))
# a, b, c

some_names = [ "John", "Jim", "James", "Jim", "Jim", "Jerry" ]

while "Jim" in some_names:
    some_names.remove("Jim")

print(some_names)
# ['John', 'James', 'Jerry']
