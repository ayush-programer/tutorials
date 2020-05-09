# Python3 Generator Examples

class Vegetables():

    def __iter__(self):

        yield "Potato"
        yield "Carrot"
        yield "Salad"
        yield "Parsley"

for vegetable in Vegetables():
    print(vegetable)
# Potato
# Carrot
# Salad
# Parsley

# Note: The yield keyword also acts as a sort
# of barrier: when called again, the function
# will resume from current yield until next

class Multiple():

    def __init__(self, k, m):

        self.k = k
        self.m = m

    def __iter__(self):

        n = 0

        while True:
            if (n > self.m):
                break

            yield n

            n += self.k

for num in Multiple(3, 10):
    print(num)
# 0
# 3
# 6
# 9

# <-- generator expression -->

n = 10
m = 3
for num in (x for x in range(0, n) if x % m == 0):
    print(num)
# 0
# 3
# 6
# 9

# Note: Unlike list comprehension, generator
# expressions and generators produce only one
# item at a time (perfect for lazy evaluation)
