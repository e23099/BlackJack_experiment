#-----------------------------------------------------
# Define Black Jack Dealer
# The Dealer should have:
#   1. hand cards (2 given at beginning)
#   2. card left  (number of cards not dealt yet)
#   3. card Dealt (a note of which cards have been dealt)
#   4. hand, maxPoint, minPoint (the same as a BJPlayer)
#
# Whenever a Dealer has only 17*nDeck cards left(one-third of the total),
# he should shuffle all cards to continue dealing.
#-----------------------------------------------------

from Card import Card
from BJPlayer import BJPlayer
from numpy import random as rn
# parameter
MIN_CARD_LEFT = 17

class BJDealer(BJPlayer):
    def __init__(self, nDeck):
        self.nDeck = nDeck
        self.cardLeft  = 52 * nDeck
        self.cardDealt = [False for i in range(52*nDeck)]
        self.hand = []
        self.maxPoint = 0
        self.minPoint = 0

    def shuffle(self):
        """shuffle all cards"""
        self.cardDealt = [False for i in range(52*self.nDeck)]

    def shuffleIfNeeded(self):
        if self.cardLeft < MIN_CARD_LEFT * self.nDeck:
            self.shuffle()

    def draw(self):
        """draw a card randomly from the shuffled decks and return the id of this card"""
        self.cardLeft -= 1
        id = rn.randint(52*self.nDeck)
        while self.cardDealt[id]:
            id = rn.randint(52*self.nDeck)
        self.cardDealt[id] = True
        return id % 52

    def start(self, card1, card2):
        """ receive 2 cards """
        self.hand = [] # discard all hand cards before a new game
        self.maxPoint = 0
        self.minPoint = 0
        self.addCard(card1)
        self.addCard(card2)


    # def addCard(self, cardID):
    #     c = Card(cardID)
    #     super().addCard(c)

    def addCards(self):
        """add cards until total points reach 17 or above"""
        while self.total() < 17:
            c = Card(self.draw())
            self.addCard(c)

    def judge(self, player: BJPlayer):
        """return 'win' or 'lose' or 'tie' of a player"""
        # case1: Dealer has BlackJack
        if self.isBlackJack():
            if player.isBlackJack():
                return 'tie'
            else:
                return 'lose'
        # case2: Dealer doesn't have BlackJack and doesn't exceed 21 points
        elif self.total() <= 21:
            if player.isBlackJack():
                return 'WIN' # "Big" WIN means winning by getting BlackJack
            elif player.total() == self.total():
                return 'tie'
            elif player.total() < self.total() or player.total() > 21:
                return 'lose'
            else:
                return 'win'
        # case3: Dealer exceed 21 points
        else:
            if player.isBlackJack():
                return 'WIN'
            elif player.total() <= 21:
                return 'win'
            else:
                return 'lose'
