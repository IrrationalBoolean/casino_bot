# Krzysztof requesting for comment regarding the direction I am taking before I proceed any further
cardsInDeck = [suit + str(val) for suit in 'CDHS' for val in [i for i in range(2, 11)] + ['J', 'Q', 'K', 'A']]

#should I just remove self._handSize from __init__ and just keep a getHandSize method that only returns the length of self._cards?
class Hand(object):
    def __init__(self):
        self._cards = []
        self._handSize = len(self._cards)

    def __len__(self):
        return len(self.getCards())

    def getCards(self, isImageOnly=False, isKeyOnly=False):
        assert type(isImageOnly) == bool and not (isImageOnly and isKeyOnly)
        try:
            if isImageOnly:
                return [list(card.values())[0] for card in self._cards]
            elif isKeyOnly:
                return [list(card.keys())[0] for card in self._cards]
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
        self.setHandSize()

    def setHandSize(self):
        self._handSize = len(self.getCards())

    def receiveCard(self, card):
        # create assertion for card
        self._cards.append(card)
        self.setHandSize()

    def discard(self, cardChoice=None):
        """
        discards a card from hand

        cardChoice: string (optional)
            assumes a string in cardsInDeck

        return: dictionary
            discarded card
        """
        assert self.getHandSize() > 0
        try:
            if cardChoice is None:
                toDiscard = self._cards.pop()
            else:
                indexOfCard = self.getCards(isKeyOnly=True).index(cardChoice.upper())
                toDiscard = self._cards.pop(indexOfCard)
            self.setHandSize()
            return toDiscard
        except (AssertionError, ValueError) as err:  # ValueError if .index() does not find cardChoice in self._hand
            print('Invalid move!')
            # invalid move operation

    def discardHand(self):
        while self.getHandSize() > 0:
            self.discard()
        self.setHandSize()


class Player(object):
    def __init__(self, buyIn, seatNum, isDealer=False):
        self._hand = Hand()
        self._balance = buyIn
        self._seatNum = seatNum
        self._isDealer = isDealer

    def getHand(self):
        return self._hand.getCards(isImageOnly=True)

    def getBalance(self):
        return self._balance

    def getSeatNum(self):
        return self._seatNum

    def getIsDealer(self):
        return self._isDealer

    def setHand(self, cards):
        self._hand.setCards(cards)

    def setBalance(self, amount):
        self._balance = amount

    def setSeatNum(self, num):
        self._seatNum = num

    def setIsDealer(self):
        if self.getIsDealer():
            self._isDealer = False
        else:
            self._isDealer = True

    def check(self):
        pass

    def bet(self, amount):
        assert type(amount) == int and (0 < amount <= self.getBalance())
        try:
            self.setBalance(self.getBalance() - amount)
            return amount
        except AssertionError:
            print('Invalid!')
            # invalid bet operation

    def call(self, toCall):
        assert type(toCall) == int
        try:
            if toCall > self.getBalance():
                self.allIn()
            else:
                self.bet(toCall)
        except AssertionError:
            print('Invalid')
            # invalid toCall

    def allIn(self):
        self.bet(self.getBalance())

    def fold(self):
        self._hand.discardHand()
