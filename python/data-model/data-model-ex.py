# Python3 Data Model Examples

from random import randint
import copy

class Card():
    """Rabu Retta card class"""

    def __init__(self, name, value, count=1):
        """Rabu Retta card init"""

        self.name = name
        self.value = value
        self.count = count

    def __repr__(self):

        return "Card(%s, %s, %s)" % (self.name, self.value, self.count)

    def __str__(self):

        return "%s (%d)" % (self.name, self.value)

# Note: str() is used to create output for end-user,
# while repr() is used for debugging purposes, i.e.
# for official representation of the object

class RabuRettaRound():
    """Rabu Retta round class"""

    # static / class variable
    card_pool = [
            Card("Princess", 8),
            Card("Countess", 7),
            Card("King", 6),
            Card("Prince", 5, 2),
            Card("Handmaid", 4, 2),
            Card("Baron", 3, 2),
            Card("Priest", 2, 2),
            Card("Guard", 1, 5)
            ]

    rounds_played = 0

    def __init__(self, players=4):
        """Rabu Retta round init"""

        if players > 4 or players < 0:
            raise Exception("Invalid number of players (2-4)")

        self.length_hash = -1
        self.players = players
        self.deck = copy.deepcopy(RabuRettaRound.card_pool)
        to_remove = randint(0, len(self) - 1)

        self.facedown = []
        self.faceup = []

        self.facedown.append(self.pop(to_remove))

        if players == 2:
            for _ in range(0, 3):
                self.faceup.append(self.pop(randint(0, len(self) - 1)))

    @staticmethod
    def print_info():
        """static method to print info"""

        print("Rabu Retta is a great game!")

    def __len__(self):
        """for len(RabuRettaRound())"""

        if self.length_hash > -1:
            return self.length_hash

        sum = 0
        for card in self.deck:
            sum += card.count
        return sum

    def __getitem__(self, index):
        """for RabuRettaRound()[index]"""

        length = len(self)

        position = index if index >= 0 else length + index

        if position >= length:
            raise IndexError

        current = 0

        for card in self.deck:

            if position >= current and position < current + card.count:
                return card

            current += card.count

        raise IndexError

    def pop(self, index=-1):
        """implement pop() method"""

        to_remove = self[index]
        del self[index]

        return to_remove

    def get_card(self):

        return self.pop(randint(0, len(self) - 1))

    def __delitem__(self, index):
        """remove card from the deck (del implementation)"""

        length = len(self)

        to_remove = index if index >= 0 else length + index

        if to_remove >= length:
            raise IndexError

        current = 0

        for card_index, card in enumerate(self.deck, start=0):

            if to_remove >= current and to_remove < current + card.count:

                if card.count == 1:
                    to_return = self.deck.pop(card_index)
                    self.length_hash -= 1
                    return to_return

                elif card.count > 1:
                    card.count -= 1
                    self.length_hash -= 1

                    return card
                else:
                    raise IndexError

            current += card.count

    def __repr__(self):

        return str(list(map(lambda card: repr(card), self.deck)))

    def __str__(self):

        display_string = "RabuRetta round for %d players." % self.players

        if self.faceup:
            display_string += (
                    "\nFaceup cards:\n\t" +
                    str(list(map(lambda card: str(card), self.faceup)))
                    )
        if self.facedown:
            display_string += (
                    "\nNumber of facedown cards: %d" % len(self.facedown)
                    )

        return display_string

    def __del__(self):
        """Called when garbage collector calls destructor"""
        RabuRettaRound.rounds_played += 1

import unittest

class RabuRettaRoundTests(unittest.TestCase):

    def test_type(self):
        """Test if type is RabuRettaRound"""

        self.assertEqual(type(RabuRettaRound()), RabuRettaRound)

    def test_players(self):
        """Test exception raising on invalid number of players"""

        for num in range(0, 4):
            if num <= 0 or num > 4:
                self.assertRaises(Exception, RabuRettaRound(num))
            else:
                try:
                    RabuRettaRound(num)
                except Exception:
                    self.fail("Number of players should be valid.")

    def test_len(self):
        """Test deck size for various player number inputs."""

        for _ in range(0, 100):
            for num in range(2, 5):
                self.assertEqual(len(RabuRettaRound(num)), 12 if num == 2 else 15)

    def test_getitem(self):
        """Test __getitem__ method"""

        for num in range(2,5):
            rrr = RabuRettaRound(num)
            rrr_length = len(rrr)
            card = None
            card_hash = {}

            for index in range(-3 - rrr_length, rrr_length + 3):

                if ((index >= rrr_length and index >= 0) or
                    (-index > rrr_length and index <= 0)):

                    with self.assertRaises(IndexError):
                        rrr[index]

                    # Note: self.assertRaises(IndexError, rrr[index])
                    # won't work because rrr[index] will raise IndexError
                    # before self.assertRaises gets called; another
                    # solution would be to make rrr[index] a method, e.g.:
                    # self.assertRaises(IndexError, lambda: rrr[index])

                else:
                    try:
                        card = rrr[index]

                    except IndexError:
                        self.fail(
                                "Index " + str(index) + " should not be " +
                                " out of bounds (length: " + str(rrr_length) + ")."
                                )

            for index in range(0, rrr_length):

                try:
                    card = rrr[index]
                    card_hash[card.name] += 1

                except KeyError:
                    card_hash[card.name] = 1

                except IndexError:
                    self.fail("Index out of bounds!")

            try:
                for card in rrr.deck:
                    self.assertEqual(card_hash[card.name], card.count)

            except KeyError:
                self.fail(card.name + " not hashed!")

    def test_iter(self):
        """Test iter and last"""

        for num in range(2, 5):

            rrr = RabuRettaRound(num)
            rrr_iter = iter(rrr)

            # Note: __getitem__ and __len__ are enough
            # to provide for __iter__

            rrr_length = len(rrr)
            item = None
            counter = 0

            while True:
                try:
                    item = next(rrr_iter)
                    self.assertTrue(counter < rrr_length)
                    counter += 1

                except StopIteration:
                    self.assertEqual(item, rrr[-1])
                    break

if __name__ == "__main__":

    import sys

    if len(sys.argv) >= 2:
        if sys.argv[1] == "test":
            unittest.main(argv=['first-arg-is-ignored'], exit=False)
            # Note: The unittest should be in a separate file,
            # so we need to hack this a bit...

        elif sys.argv[1] == "info":
            RabuRettaRound.print_info()

        else:
            print(
                    "Use 'test' option to run unit tests "
                    "and 'info' to get information on RabuRetta"
                    )
    else:
        rrr = RabuRettaRound(2)
        print(rrr)
        print("You got the card from the deck:\n\t" + str(rrr.get_card()))
