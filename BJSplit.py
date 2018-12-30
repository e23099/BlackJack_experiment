from BJPlayer import BJPlayer
from Card import Card

class BJSplit(BJPlayer):
    def __init__(self, betAmt, card: Card):
        self.__capital = 0
        self.hand = []  # a null array to store hand cards
        self.maxPoint = 0
        self.minPoint = 0
        self.betAmt = betAmt
        self.addCard(card)

    def start(self): # no start() is needed
        pass
    def splitHand(self): # can only split once
        pass
    def bet(self): # no further bet is needed
        pass

    def doubleBet(self, cashRemain):
        """when player has enough money to double the bet, return True"""
        if cashRemain >= self.betAmt: # if super() has enough capital to doubleBet
            self.betAmt *= 2
            return True
        return False

    def endSplit(self):
        """when the split round is over, send the bet earned (if any) to original player"""
        if self.__capital > 0:
            return self.__capital
        return 0

    def earn(self, amt):
        self.__capital += amt