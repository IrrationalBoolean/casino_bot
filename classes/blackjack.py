import random
from classes.base_classes import Hand, Player, Game

class BlackJackHand(Hand):
    VALUES = dict(**{str(x) : x for x in range(2,10)},
                  **{y: 10 for y in list("0KJQ")},
                  **{"A": 11})

    def __init__(self):
        super().__init__()

    def __eq__(self, other):
        if not isinstance(other, BlackJackHand):
            return TypeError("Can only compare BlackJackHand with"
                             " another BlackJackHand")
        return self.tabulate_score() == other.tabulate_score()

    def __ne__(self, other):
        if not isinstance(other, BlackJackHand):
            return TypeError("Can only compare BlackJackHand with"
                             " another BlackJackHand")
        return self.tabulate_score() != other.tabulate_score()

    def __lt__(self, other):
        if not isinstance(other, BlackJackHand):
            return TypeError("Can only compare BlackJackHand with"
                             " another BlackJackHand")
        return self.tabulate_score() < other.tabulate_score()

    def __gt__(self, other):
        if not isinstance(other, BlackJackHand):
            return TypeError("Can only compare BlackJackHand with"
                             " another BlackJackHand")
        return self.tabulate_score() > other.tabulate_score()


    def tabulate_score(self):
        if not self.cards:
            return 0
        aces = sum([1 for card in self if card[1] == "A"])
        score = sum([self.VALUES[card[-1]] for card in self])
        while score > 21 and aces:
            score -= 10
            aces -= 1
        if score > 21:
            return -1
        return score


class BlackJackPlayer(Player):
    def __init__(self, buyin, is_dealer=False):
        super().__init__(buyin, is_dealer=is_dealer)



class BlackJackGame(Game):
    MAX_SEATS = 8
    FULL_DECK = [suit + str(val) for suit in 'CDHS' for val in [i for i in range(2, 11)]
                 + ['J', 'Q', 'K', 'A']]

    def __init__(self):
        super().__init__()
        self.table = [None for _ in range(self.MAX_SEATS)]
        self.table[0] = BlackJackPlayer(0,  is_dealer=True)
        self.players = sum([1 for seat in self.table if seat])
        self.discarded = []
        self.cards = self.FULL_DECK[:]
        random.shuffle(self.cards)

    def seat(self, player: BlackJackPlayer):
        if self.players == self.MAX_SEATS:
            print(self.players)
            return False
        for idx, seat in enumerate(self.table):
            if seat is None:
                self.table[idx] = player
                self.players = sum([1 for seat in self.table if seat])
                player.seat = idx
                return idx

    def start(self):
        for player in self.table:
            if player is not None:
                player.hand = BlackJackHand()
        while 0 <= min([player.hand.tabulate_score() for player in self.table if player]) < 17:
            for player in self.table:
                if player is not None:
                    if 0 <= player.hand.tabulate_score() < 17:
                        player.hand += self.cards.pop()
        for player in self.table:
            if player is not None:
                print(player.hand, player.hand.tabulate_score())
