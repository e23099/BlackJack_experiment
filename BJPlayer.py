#-----------------------------------------------------
# Define Black Jack Player
# Each player should have:
#   1. hand cards (2 given at beginning)
#   2. initial capital (amount of money to start playing)
#   3. maxPoint   (if Ace is in hand, maxPoint != minPoint)
#   4. minPoint   (if don't has Ace,  maxPoint == minPoint)
#   5. bet        (amount of money bet in a game)
#   6. round      (number of rounds played)
#-----------------------------------------------------

from Card import cardPat
from Card import Card

class BJPlayer():
    def __init__(self, capital):
        self.__capital = capital
        self.hand = [] # a null array to store hand cards
        self.maxPoint = 0
        self.minPoint = 0
        self.betAmt = 0
        self.round = 0

    def start(self, card1, card2):
        """ receive 2 cards """
        self.hand = [] # discard all hand cards before a new game
        self.maxPoint = 0
        self.minPoint = 0
        self.addCard(card1)
        self.addCard(card2)
        self.round += 1

    def addCard(self, card:Card):
        """ add a new card to hand """
        point = min(card.face, 9) + 1 # 10,J,Q,K all has 10 points
        # calculate maxPoint
        self.hand.append(card)
        if card.face == 0 and self.minPoint == self.maxPoint:
            self.maxPoint += 11
        elif card.face == 0 and self.minPoint != self.maxPoint:
            self.maxPoint += 1 # only one Ace should be treated as 11
        else:
            self.maxPoint += point
        # calculate minPoint
        self.minPoint += point

    def total(self):
        """ return total points to dealer """
        if self.maxPoint <= 21:
            return self.maxPoint
        else:
            return self.minPoint

    def bet(self, amt):
        """
        when player has enough money, return true and decrease amt from capital
        when player has less then enough, return false and do nothing
        """
        if self.__capital < amt:
            print("Not enough money left at round:", self.round)
            return False
        else:
            self.__capital -= amt
            self.betAmt = amt
            return True

    def doubleBet(self):
        """when player has enough money, double the bet"""
        if self.__capital >= self.betAmt:
            self.__capital -= self.betAmt
            self.betAmt *= 2
            return True
        return False

    def splitHand(self):
        """
        When split, put away one hand card and recalculate Points
        return a card if successfully do so, otherwise return None
        """
        cardRemain = self.hand[0]
        cardSplit = self.hand[1]
        if min(cardRemain.face, 9) != min(cardSplit.face, 9):
            return None  # if split is illegal, return None
        if self.bet(self.betAmt): # if legal and able to bet another betAmt, spend the betAmt
            self.hand = []
            self.minPoint = 0
            self.maxPoint = 0
            self.addCard(cardRemain)
            return cardSplit

        return None

    def earn(self, amt):
        self.__capital += amt

    def isBlackJack(self):
        """check if got BlackJack (and Ace and a 10)"""
        if self.total() == 21 and len(self.hand) == 2:
            return True
        return False

    def showHand(self, openFirst=True):
        if len(self.hand) == 0:
            return None
        for line in range(11):
            if not openFirst:
                    print(cardPat[13][line], " ", end="")
            else:
                print(cardPat[self.hand[0].face][line].replace('x', "SHDC"[self.hand[0].suit]), " ", end="")
            for card in self.hand[1:]:
                print(cardPat[card.face][line].replace('x', "SHDC"[card.suit]), " ", end="")
            print() # change line at the end

    def cashRemain(self):
        return self.__capital