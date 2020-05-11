# Python3 Data Model Examples

class Vegetables():

    def __init__(self):
        self.veggies = {
            "Potato": 3,
            "Carrot": 5,
            "Parsley": 2
                }

    def __len__(self):

        if not hasattr(self, "length"):
            self.length = sum([v for v in self.veggies.values()])

        return self.length

    def __getitem__(self, index):
        pos = index if index >= 0 else len(self) + index

        if pos >= len(self):
            raise IndexError
        else:
            true_pos = 0
            for veggie, count in self.veggies.items():
                if pos >= true_pos  and pos < true_pos + count:
                    return veggie
                else:
                    true_pos += count
        raise IndexError

    def __delitem__(self, index):
        to_del = self[index]
        if self.veggies[to_del] > 1:
            self.veggies[to_del] -= 1
        else:
            del self.veggies[to_del]
        self.length -=1

    def __repr__(self):

        return str(self.veggies)

    def __str__(self):

        return (
                "Here we have some vegetables: " +
                str([v for v in self.veggies.keys()])
                )

vegetables = Vegetables()

print(vegetables)
# Here we have some vegetables: ['Potato', 'Carrot', 'Parsley']

for veggie in vegetables:
    print(veggie)
# Potato
# Potato
# Potato
# Carrot
# Carrot
# Carrot
# Carrot
# Carrot
# Parsley
# Parsley

del vegetables[0]
del vegetables[0]
del vegetables[0]

print(repr(vegetables))
# {'Carrot': 5, 'Parsley': 2}

print(len(vegetables))
# 7

print(
        "\n"
        "To get a more comprehensive list on generic, "
        "callable and container types, visit:\n\n\t"
        "https://docs.python.org/3/reference/"
        "datamodel.html#emulating-generic-types"
        "\n"
        )
