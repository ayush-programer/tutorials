# Python3 Number Data Model Examples

class ModularInt():

    def __init__(self, val, mod):
        self.mod = mod
        self.val = val

        if val > 0 and val >= mod:
            self.val = val % mod
        elif val < 0:
            self.val += (-val // mod) * mod

    def __str__(self):
        return "%d_[%d]" % (self.val, self.mod)

    def __repr__(self):
        return "ModularInt(%d, %d)" % (self.val, self.mod)

    def check_mod(self, other):
        if other.mod != self.mod:
            raise Exception(
                    "The modular integers " + str(self) +
                    " and " + str(other) + " belong to " +
                    "different groups."
                    )

    def __add__(self, other):
        self.check_mod(other)
        return (self.val + other.val) % self.mod

    def __mul__(self, other):
        self.check_mod(other)
        return (self.val * other.val) % self.mod

print(ModularInt(3, 7) + ModularInt(5, 7))
print(ModularInt(-11, 7) + ModularInt(4, 7))
print(ModularInt(3, 5) + ModularInt(3, 3))
