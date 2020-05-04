# Python3 Class Examples

from captain import Captain

class Starship():
    """This is a simple Starship class.""" # docstring

    # self is required first argument for every method
    def __init__(self, name, captain):
        self.name = name
        self.captain = captain
        self.stardate = 0

    def engage(self, warp=9):
        print("Warp " + str(warp) + ", engage!")

    def raise_shields(self):
        print("Raising shields.")

# Note: In Python2, class has to be defined with
# object in parentheses, e.g.:
# class Starship(object)

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

    def __init__(self, captain):
        super().__init__("Unknown", captain)
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
