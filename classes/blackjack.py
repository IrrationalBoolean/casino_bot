from classes.base_classes import Hand, Player

class BlackJackHand(Hand):
    VALUES = dict(**{str(x) : x for x in range(2,10)}, **{y: 10 for y in list("0KJQ")}, **{"A": 11})

    def __init__(self):
        super().__init__()

    def __iter__(self):
        return iter(self._cards)

    def __repr__(self):
         return repr(self.cards)

    def __eq__(self, other):
        if not isinstance(other, BlackJackHand):
            return TypeError("Can only compare BlackJackHand with another BlackJackHand")
        return self.tabulate_score() == other.tabulate_score()

    def __ne__(self, other):
        if not isinstance(other, BlackJackHand):
            return TypeError("Can only compare BlackJackHand with another BlackJackHand")
        return self.tabulate_score() != other.tabulate_score()

    def __lt__(self, other):
        if not isinstance(other, BlackJackHand):
            return TypeError("Can only compare BlackJackHand with another BlackJackHand")
        return self.tabulate_score() < other.tabulate_score()

    def __gt__(self, other):
        if not isinstance(other, BlackJackHand):
            return TypeError("Can only compare BlackJackHand with another BlackJackHand")
        return self.tabulate_score() > other.tabulate_score()

    def tabulate_score(self):
        if not self._cards:
            return 0
        aces = sum([1 for card in self if card[1] == "A"])

        score = sum([self.VALUES[card[-1]] for card in self])
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

