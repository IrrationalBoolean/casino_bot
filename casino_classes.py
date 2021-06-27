# Krzysztof requesting for comment regarding the direction I am taking before I proceed any further
cardsInDeck = [suit + str(val) for suit in 'cdhs' for val in [i for i in range(2, 11)] + ['j', 'q', 'k', 'a']]

class Hand(object):
    def __init__(self):
        self._cards = {}
        self._handSize = len(self._cards)

    def getCards(self, imageOnly=False):
        assert type(imageOnly) == bool
        try:
            if imageOnly:
                return self._cards.values()
            else:
                return self._cards
        except AssertionError:
            pass
            # invalid request operation

    def getHandSize(self):
        return self._handSize

    def setCards(self, cards):
        # create assertion for cards
        self._cards = cards

    def receiveCard(self, card):
        # create assertion for card
        self._cards.update(card)

    def discard(self, cardChoice = None):
        """
        discards a card from hand, to discard entire hand perform while self.getHandize > 0 self.discard()

        cardChoice: string (optional)
            assumes a string in cardsInDeck

        return: dictionary
            discarded card
        """
        assert self.getHandSize() > 0
        try:
            if cardChoice is None:
                return {list(self.getCards())[-1]: self._cards.pop(list(self.getCards())[-1])}
            else:
                if cardChoice.lower() in self.getCards():
                    return {cardChoice.lower(): self._cards.pop(cardChoice)}
                else:
                    raise AssertionError
        except AssertionError:
            print('Invalid move!')
            # invalid move operation


class Player(object):
    def __init__(self, buyIn):
        self.balance = buyIn
        self.hand = Hand()

    pass


