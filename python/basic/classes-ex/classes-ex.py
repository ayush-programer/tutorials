# Python3 Class Examples

from captain import Captain

class Starship():
    """This is a simple Starship class.""" # docstring

    # self is required first argument for every method
    def __init__(self, name, captain):
        self.name = name
        self.captain = captain
        self.stardate = 0

    @staticmethod
    def createStarshipUFO():
        return Starship(name="X", captain="Y")

    @classmethod
    def createUFO(cls):
        return cls(name="X", captain="Y")

    def engage(self, warp=9):
        print("Warp " + str(warp) + ", engage!")

    def raise_shields(self):
        print("Raising shields.")

# Note: In Python2, class has to be defined with
# object in parentheses, e.g.:
# class Starship(object)

if __name__ == "__main__":

    # Note: Code inside the block will only be executed
    # if the module is run directly, not if it is imported

    enterprise = Starship("Enterprise", Captain("Jean-Luc", "Picard"))

    print(
            "Created " + enterprise.name +
            " and assigned it to " + enterprise.captain.get_name() + "."
            )
    # Created Enterprise and assigned it to Jean-Luc Picard.

    if enterprise.stardate == 0:
        print("Strange stardate found.")
    # Strange stardate found.

    enterprise.engage()
    # Warp 9, engage!

class KlingonStarship(Starship):
    """Specialized Klingon Starship class."""

    def __init__(self, captain, name="Unknown"):
        super().__init__(name, captain)
        self.lasers = True

# Note: In Python2, this would have to be:
# super(KlingonStarship, self).__init__("Unknown", captain)

    def fire(self):
        if self.lasers:
            print(
                    "Stardate " + str(self.stardate) +
                    ": Firing all lasers!"
                    )
        else:
            print(
                    "Stardate " + str(self.stardate) +
                    ": We can't fire lasers."
                    )

    def raise_shields(self):
        print("Klingon shields raised.")

if __name__ == "__main__":

    klingon_ship = KlingonStarship(Captain(name="Worf"))

    print(
            "Created Klingon Starship " + klingon_ship.name +
            " with captain " + klingon_ship.captain.get_name() + "."
            )
    # Created Klingon Starship Unknown with captain Worf.

    klingon_ship.fire()
    # Stardate 0: Firing all lasers!

    klingon_ship.stardate = 9000
    klingon_ship.lasers = False

    klingon_ship.fire()
    # Stardate 9000: We can't fire lasers.

    enterprise.raise_shields()
    # Raising shields.

    klingon_ship.raise_shields()
    # Klingon shields raised.

    # <-- classmethod factory -->

    ss = Starship.createUFO()
    print(("is Klingon" if isinstance(ss, KlingonStarship) else "is not Klingon")
            + " with " + ss.name + " name and " + ss.captain + " captain")
    # is not Klingon with X name and Y captain

    kss = KlingonStarship.createUFO()
    print(("is Klingon" if isinstance(kss, KlingonStarship) else "is not Klingon")
            + " with " + kss.name + " name and " + kss.captain + " captain")
    # is Klingon with X name and Y captain

    # <-- staticmethod factory -->

    kss = KlingonStarship.createStarshipUFO()
    print(("is Klingon" if isinstance(kss, KlingonStarship) else "is not Klingon")
            + " with " + kss.name + " name and " + kss.captain + " captain")
    # is not Klingon with X name and Y captain

    # <-- copying objects -->

    klingon_ship_copy = klingon_ship
    klingon_ship_copy.stardate = 0
    klingon_ship.fire()
    # Stardate 0: We can't fire lasers.

    # Note: Both klingon_ship_copy and klingon_ship
    # point to the same object

    import copy

    klingon_ship_shallow_copy = copy.copy(klingon_ship)
    klingon_ship_shallow_copy.stardate = 5000
    klingon_ship.fire()
    # Stardate 0: We can't fire lasers.

    # <-- shallow copy -->

    klingon_array = [ klingon_ship ]

    klingon_array_copy = klingon_array[:]
    klingon_array_copy[0].stardate = 5000
    klingon_ship.fire()
    # Stardate 5000: We can't fire lasers.

    klingon_array_shallow_copy = copy.copy(klingon_array)
    klingon_array_shallow_copy[0].stardate = 9000
    klingon_ship.fire()
    # Stardate 9000: We can't fire lasers.

    # <-- deep copy -->

    klingon_array_deep_copy = copy.deepcopy(klingon_array)
    klingon_array_deep_copy[0].stardate = 5000
    klingon_ship.fire()
    # Stardate 9000: We can't fire lasers.

    # Note: Shallow copy (copy.copy()) copies the object,
    # but it is deep copy (copy.deepcopy()) that copies
    # the object recursively. Note that shallow copy with
    # regard to lists is the same as array1 = array2[:]
