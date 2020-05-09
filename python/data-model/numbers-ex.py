# Python3 Number Data Model Examples

class ModularInt():

    def __init__(self, val, mod):
        self.mod = mod
        self.val = val

        if val > 0 and val >= mod:
            self.val = val % mod
        elif val < 0:
            self.val += (-val // mod) * (mod + 1)

    def __str__(self):
        return str(self.value) + "_[" + str(mod) + "]"

    def __repr__(self):
        return self.__str__()

    def check_mod(self, other):
        if other.mod != self.mod:
            raise Exception(
                    "The modular integers " + str(self) +
                    " and " + str(other) + " belong to " +
                    "different groups."
                    )

    def __add__(self, other):
        self.check_mod(self, other)
        return (self.val + other.val) % self.mod

    def __mul__(self, other):
        self.check_mod(self, other)
        return (self.val * other.val) % self.mod
