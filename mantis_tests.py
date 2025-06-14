from mantis_game import *
import unittest

def make_player(colors):
    p = Player()
    for c in colors:
        p.receive_card(Card(c, None))

    return p

class TestPlayer(unittest.TestCase):
    def test_score(self):
        p = make_player(["red", "red", "red"])

        self.assertEqual(len(p.contained_cards), 3)
        self.assertEqual(p.points(), 0)
        
        p.score(Card("red", None))

        self.assertEqual(len(p.contained_cards), 0)
        self.assertEqual(p.points(), 4)

    def test_score2(self):
        p = make_player(["redge", "red", "blue", "red", "red"])

        self.assertEqual(len(p.contained_cards), 5)
        self.assertEqual(p.points(), 0)
        
        p.score(Card("red", None))

        self.assertEqual(len(p.contained_cards), 2)
        self.assertEqual(p.points(), 4)

    def test_remove_colored_cards(self):
        p = make_player(["blue", "green", "yellow", "green", "blue", "pink"])

        self.assertEqual(len(p.contained_cards), 6)
        self.assertEqual(p.points(), 0)
        colors = [c.color for c in p.contained_cards]
        self.assertEqual(colors.count("blue"), 2)
        self.assertEqual(colors.count("green"), 2)
        self.assertEqual(colors.count("yellow"), 1)
        self.assertEqual(colors.count("pink"), 1)

        p.remove_color("blue!")
        self.assertEqual(len(p.contained_cards), 6)
        self.assertEqual(p.points(), 0)

        p.remove_color("blue")
        self.assertEqual(len(p.contained_cards), 4)
        self.assertEqual(p.points(), 0)

        p.remove_color("blue")
        self.assertEqual(len(p.contained_cards), 4)
        self.assertEqual(p.points(), 0)

        p.remove_color("yellow")
        self.assertEqual(len(p.contained_cards), 3)
        self.assertEqual(p.points(), 0)

    def test_get_same_color_cards(self):
        pass

class TestDeck(unittest.TestCase):
    def test_card_invariants(self):
        pass

    def test_deck_invariants(self):
        pass

    def test_shuffle(self):
        pass


if __name__ == '__main__':
    unittest.main()