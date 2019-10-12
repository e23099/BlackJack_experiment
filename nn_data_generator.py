from Card import Card
from BJDealer import BJDealer
from BJPlayer import BJPlayer
import copy
from numpy import random as rn

class KnownCards():
    def __init__(self):
        self.cardList = []
        self.nCard = 0
        self.nTen = 0
        self.nOne = 0
        self.nAce = 0

    def add(self, card:Card):
        if card.face == 0:
            self.nAce += 1
        elif card.face > 8:
            self.nTen += 1
        else:
            self.nOne += 1
        self.nCard += 1
        self.cardList.append(card)

    def printData(self):
        out = ""
        out += str(self.nCard) + ","
        out += str(self.nTen) + ","
        out += str(self.nOne) + ","
        out += str(self.nAce) + ","
        return out

    def reset(self):
        self.__init__()


class Recorder():
    def __init__(self, dataPath):
        self.dataPath = dataPath
        self.records = []
        self.nRecord = 0
        self.history = {}
        with open('nn_history_expectation.csv', 'r') as f:
            lines = f.readlines()
            for line in lines:
                row = line.split(',')
                self.history[row[0]] = {'avg': (float)(row[1]), 'cnt': (int)(row[2])}


    def add(self, k: KnownCards, small:int, large:int, isFirst:int, canSplit:int, dealerHand:int, nDeck:int, action:int, profit:float):
        row = k.printData()
        row += str(small) + ','
        row += str(large) + ','
        row += str(isFirst) + ','
        row += str(canSplit) + ','
        row += str(dealerHand) + ','
        row += str(nDeck) + ','
        row += str(action) + ','
        row += str(profit) + '\n'
        self.records.append(row)
        self.nRecord += 1

    def printResult(self):
        for row in self.records:
            print(row)

    def updateAverage(self, small, large, result):
        if small == large:
            hand = str(small)
        else:
            hand = 'A' + str(small - 1)
        n = (int)(self.history[hand]['cnt'])
        self.history[hand]['avg'] = (self.history[hand]['avg']*n + result) / (n+1)
        self.history[hand]['cnt'] += 1

    def ExpectedScore(self, c1:Card, c2:Card):
        player = BJPlayer(0)
        player.addCard(c1)
        player.addCard(c2)
        if player.minPoint == player.maxPoint:
            return self.history[str(player.minPoint)]['avg']
        else:
            return self.history['A' + str(player.minPoint-1)]['avg']

    def EndTask(self):
        with open(self.dataPath+'.csv', 'w+') as f:
            for row in self.records:
                f.write(row)

        with open('nn_history_expectation.csv', 'w') as f:
            for row in self.history:
                f.write(str(row) + ',' + str(self.history[row]['avg']) + ',' + str(self.history[row]['cnt']) + '\n')
        self.records = []
        self.nRecord = 0


def DealerShowHandsFirst(dealer: BJDealer, known: KnownCards):
    dealer.addCards()
    known.add(dealer.hand[0]) # first card of dealer is shown to player

def AddTwoCardsToPlayer(dealer: BJDealer, player: BJPlayer, known: KnownCards):
    c1 = Card(dealer.draw())
    c2 = Card(dealer.draw())
    player.addCard(c1)
    player.addCard(c2)
    known.add(c1)
    known.add(c2)

def Score(dealer: BJDealer, player: BJPlayer):
    """return 'win' or 'lose' or 'tie' of a player"""
    # case1: Dealer has BlackJack
    if dealer.isBlackJack():
        if player.isBlackJack():
            return 0.0
        else:
            return -1.0
    # case2: Dealer doesn't have BlackJack and doesn't exceed 21 points
    elif dealer.total() <= 21:
        if player.isBlackJack():
            return 1.5 # "Big" WIN means winning by getting BlackJack
        elif player.total() == dealer.total():
            return 0.0
        elif player.total() < dealer.total() or player.total() > 21:
            return -1.0
        else:
            return 1.0
    # case3: Dealer exceed 21 points
    else:
        if player.isBlackJack():
            return 1.5
        elif player.total() <= 21:
            return 1.0
        else:
            return -1.0

def getDealerShownCard(dealer: BJDealer):
    return FaceOfCard(dealer.hand[0])

def FaceOfCard(card:Card):
    if card.face == 0:
        return 11
    if card.face > 8:
        return 10
    return card.face+1

def CanSplitHand(player: BJPlayer):
    if len(player.hand) > 2:
        return 0
    if FaceOfCard(player.hand[0]) != FaceOfCard(player.hand[1]):
        return 0
    return 1


def SudoStop(record, memory, player, dealer, bestResult):
    profit = Score(dealer, player)
    record.add(
        memory,
        player.minPoint,
        player.maxPoint,
        1 if len(player.hand) == 2 else 0,
        CanSplitHand(player),
        getDealerShownCard(dealer),
        dealer.nDeck,
        2,
        profit
    )
    bestResult.append(profit)

def SudoGiveUp(record, memory, player, dealer):
    record.add(
        memory,
        player.minPoint,
        player.maxPoint,
        1,
        CanSplitHand(player),
        getDealerShownCard(dealer),
        dealer.nDeck,
        5,
        -0.5
    )

def SudoDouble(record, memory, player: BJPlayer, dealer:BJDealer, card, bestResult):
    copyPlayer = copy.deepcopy(player)
    copyPlayer.addCard(card)
    profit = Score(dealer, copyPlayer)*2
    record.add(
        memory,
        player.minPoint,
        player.maxPoint,
        1,
        CanSplitHand(player),
        getDealerShownCard(dealer),
        dealer.nDeck,
        3,
        profit
    )
    bestResult.append(profit)

def SudoMoreCard(record, memory, player:BJPlayer, dealer:BJDealer, card, bestResult):
    copyPlayer = copy.deepcopy(player)
    copyPlayer.addCard(card)
    profit = Score(dealer, copyPlayer) if copyPlayer.minPoint > 21 else 0
    record.add(
        memory,
        player.minPoint,
        player.maxPoint,
        1 if len(player.hand) == 2 else 0,
        CanSplitHand(player),
        getDealerShownCard(dealer),
        dealer.nDeck,
        1,
        profit
    )
    bestResult.append(profit)

def SudoSplit(record, memory, player:BJPlayer, dealer:BJDealer):
    copyDealer = copy.deepcopy(dealer)
    c1 = Card(copyDealer.draw())
    c2 = Card(copyDealer.draw())
    # print('(' + str(FaceOfCard(c1)) + ', ' + str(FaceOfCard(player.hand[0])) + ')')
    # print('(' + str(FaceOfCard(c2)) + ', ' + str(FaceOfCard(player.hand[0])) + ')')
    profit = record.ExpectedScore(player.hand[0], c1) + record.ExpectedScore(player.hand[1], c2)
    record.add(
        memory,
        player.minPoint,
        player.maxPoint,
        1,
        CanSplitHand(player),
        getDealerShownCard(dealer),
        dealer.nDeck,
        4,
        profit
    )

def resetPlayer(player: BJPlayer):
    player.hand = []
    player.minPoint = 0
    player.maxPoint = 0

def oneRound(dealer, player, memory, record):
    DealerShowHandsFirst(dealer, memory)
    AddTwoCardsToPlayer(dealer, player, memory)
    bestResult = [-0.5]
    initHands = [player.minPoint, player.maxPoint]

    # 模擬停牌
    SudoStop(record, memory, player, dealer, bestResult)
    # 模擬投降
    SudoGiveUp(record, memory, player, dealer)

    # 模擬分牌
    if (FaceOfCard(player.hand[0]) == FaceOfCard(player.hand[1])):
        SudoSplit(record, memory, player, dealer)

    # 模擬 double 和 加牌
    c1 = Card(dealer.draw())
    SudoDouble(record, memory, player, dealer, c1, bestResult)
    SudoMoreCard(record, memory, player, dealer, c1, bestResult)
    player.addCard(c1)
    memory.add(c1)

    # 模擬後續加牌/停牌
    while player.minPoint < 21:
        c = Card(dealer.draw())
        SudoMoreCard(record, memory, player, dealer, c, bestResult)
        SudoStop(record, memory, player, dealer, bestResult)
        player.addCard(c)
        memory.add(c)

    record.updateAverage(initHands[0], initHands[1], sum(bestResult)/len(bestResult))
    for card in dealer.hand[1:]:
        memory.add(card)
    resetPlayer(player)
    resetPlayer(dealer)

if __name__ == '__main__':
    rn.seed(600)
    # 1 deck, 1000 round
    dealer = BJDealer(1)
    player = BJPlayer(0)
    memory = KnownCards()
    record = Recorder('nn_deck_1_round_2000')

    for i in range(30000):
        oneRound(dealer, player, memory, record)
        if dealer.cardLeft < 17 * dealer.nDeck:
            memory.reset()
            dealer.shuffle()

    record.EndTask()


    # 6 deck, 1000 round
    dealer = BJDealer(6)
    player = BJPlayer(0)
    memory = KnownCards()
    record = Recorder('nn_deck_6_round_2000')

    for i in range(30000):
        oneRound(dealer, player, memory, record)
        if dealer.cardLeft < 17 * dealer.nDeck:
            memory.reset()
            dealer.shuffle()

    record.EndTask()

