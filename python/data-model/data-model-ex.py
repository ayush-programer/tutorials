# Python3 Data Model Examples

from random import randint
import copy
import unittest

class Card():
    """Rabu Retta card class"""

    def __init__(self, name, value, count=1):
        """Rabu Retta card init"""

        self.name = name
        self.value = value
        self.count = count

    def __repr__(self):
        """for print()"""

        return self.name + " (" + str(self.count) + ")"

    def __str__(self):
        """for str()"""

        return self.__repr__()

class RabuRettaRound():
    """Rabu Retta round class"""

    # static variable
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

    def __init__(self, players=4):
        """Rabu Retta round init"""

        if players > 4 or players < 0:
            raise Exception("Invalid number of players (2-4)")

        self.deck = copy.deepcopy(RabuRettaRound.card_pool)
        self.facedown = self.remove_card(randint(0, len(self) - 1))
        self.faceup = []

        if players == 2:
            for _ in range(0, 3):
                self.faceup.append(self.remove_card(randint(0, len(self) - 1)))

    def __len__(self):
        """for len(RabuRettaRound())"""

        sum = 0
        for card in self.deck:
            sum += card.count
        return sum

    def remove_card(self, to_remove):
        """remove card from the deck method"""

        length = len(self)

        if 0 > to_remove or to_remove >= length:
            raise IndexError

        current = 0

        for index, card in enumerate(self.deck, start=0):

            if to_remove >= current and to_remove <= current + card.count:

                if card.count == 1:
                    return self.deck.pop(index)
                elif card.count > 1:
                    card.count -= 1
                    return card
                else:
                    raise IndexError

            current += card.count

class RabuRettaRoundTests(unittest.TestCase):

    def test_players(self):
        """Test exception raising on invalid number of players"""

        for num in range(0, 4):
            if num <= 0 or num > 4:
                self.assertRaises(Exception, RabuRettaRound(num))
            else:
                try:
                    RabuRettaRound(num)
                except Exception:
                    self.fail("Should not raise exception")

    def test_len(self):
        """Test deck size for various player number inputs."""

        for _ in range(0, 100):
            for num in range(2, 5):
                self.assertEqual(len(RabuRettaRound(num)), 12 if num == 2 else 15)

unittest.main()
