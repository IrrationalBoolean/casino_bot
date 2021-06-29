# Krzysztof requesting for comment regarding the direction I am taking before I proceed any further
cardsInDeck = [suit + str(val) for suit in 'CDHS' for val in [i for i in range(2, 11)] + ['J', 'Q', 'K', 'A']]


class Hand(object):
    def __init__(self):
        self._cards = []

    def __len__(self):
        return len(self.cards)

    def __iadd__(self, card):
        if type(card) == list:
            self.cards += card
        else:
            self.cards += [card]
        return self

    @property
    def cards(self):
        return self.getCards()

    @cards.setter
    def cards(self, cards):
        # create assertion for cards
        if type(cards) == list:
            self._cards = cards
        else:
            self._cards = [cards]

    def getCards(self, isKeyOnly: bool = False, isImageOnly: bool = False) -> list:
        assert (type(isImageOnly) == bool and type(isKeyOnly) == bool) and not (isImageOnly and isKeyOnly)
        try:
            if isImageOnly:
                return [list(card.values())[0] for card in self._cards][:]
            elif isKeyOnly:
                return [list(card.keys())[0] for card in self._cards][:]
            else:
                return self._cards[:]
        except AssertionError:
            pass
            # invalid request operation

    def discard(self, cardChoice=None):
        """
        discards a card from hand

        cardChoice: string (optional)
            assumes a string in cardsInDeck

        return: dictionary
            discarded card
        """
        assert len(self) > 0
        try:
            if cardChoice is None:
                toDiscard = self._cards.pop()
            else:
                indexOfCard = self.getCards(isKeyOnly=True).index(cardChoice.upper())
                toDiscard = self._cards.pop(indexOfCard)
            return toDiscard
        except (AssertionError, ValueError) as err:  # ValueError if .index() does not find cardChoice in self._cards
            print('Invalid move!')
            # invalid move operation

    def discardHand(self):
        while len(self) > 0:
            self.discard()


class Player(object):
    def __init__(self, buyIn, seatNum, isDealer=False):
        self._balance = buyIn
        self._seatNum = seatNum
        self._isDealer = isDealer

    def __iadd__(self, amount):
        self.balance = self.balance + amount
        return self

    def __isub__(self, amount):
        self.balance = self.balance - amount
        return self

    @property
    def balance(self):
        return self._balance

    @property
    def seatNum(self):
        return self._seatNum

    @property
    def isDealer(self):
        return self._isDealer

    @balance.setter
    def balance(self, amount):
        self._balance = amount

    @seatNum.setter
    def seatNum(self, num):
        self._seatNum = num

    @isDealer.setter
    def isDealer(self, button: bool):
        self._isDealer = button

    def check(self):
        pass

    def bet(self, amount: int) -> int:
        assert type(amount) == int and (0 < amount <= self.balance)
        try:
            self.balance -= amount
            return amount
        except AssertionError:
            print('Invalid!')
            # invalid bet operation

    def call(self, toCall: int):
        assert type(toCall) == int
        try:
            if toCall > self.balance:
                self.allIn()
            else:
                self.bet(toCall)
        except AssertionError:
            print('Invalid')
            # invalid toCall

    def allIn(self):
        self.bet(self.balance)
