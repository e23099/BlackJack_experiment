#-----------------------------------------------------
# Define a Gaming system that allows Player to start a game,
# add cards, bet and get returns.
#
# In this Gaming system, we should control behaviors of players
# and dealers alike. All the rules of the BlackJack Game are
# also implemented in this module.
#-----------------------------------------------------

from BJPlayer import BJPlayer
from BJDealer import BJDealer
from BJSplit import  BJSplit
from Card import Card

from numpy import random as rn
# parameters

BJBONUS = 1.5


class BJGameMove():
    def __init__(self, player: BJPlayer, dealer: BJDealer):
        self.player = player
        self.dealer = dealer
        self.playing = False
        self.splitting = False
        self.doneSplitHand = False
        print("Game Start")

    def newGame(self, amt):
        if self.playing:
            print("This round is not over. [newGame called]")
            return False

        self.dealer.shuffleIfNeeded()
        # case1: enough money for new bet
        if self.player.bet(amt):
            c1 = Card(self.dealer.draw())
            c2 = Card(self.dealer.draw())
            self.player.start(c1, c2)      # 2 cards for player
            c3 = Card(self.dealer.draw())
            c4 = Card(self.dealer.draw())
            self.dealer.start(c3, c4)      # 2 cards for dealer
            self.playing = True
            self.doneSplitHand = False
            return True
        # case2: not enough money for new bet
        else:
            print("You have no money. [newGame called]")
            return False

    def moreCard(self):
        if not self.playing:
            print("Bet for new round first. [moreCard called]")
            return False

        if self.player.total() >21:
            print("Already exceed 21 [moreCard called]")
            return False

        else:
            c = Card(self.dealer.draw())
            self.player.addCard(c)
            return True

    def giveUp(self):
        if not self.playing:
            print("Bet for new round first. [giveUp called]")
            return False
        if self.splitting:
            print("Split already, cannot give up.")
            return False

        self.player.earn(self.player.betAmt // 2)
        self.playing = False
        return True

    def __collectMoney(self, bjp ):
        """ after dealer do the job, maintain the bet for the given player"""
        # Dealer judge and give/collect bet
        result = self.dealer.judge(bjp)
        if result == 'tie': # return bet
            bjp.earn(bjp.betAmt)
        elif result == 'win': # double return bet
            bjp.earn(bjp.betAmt * 2)
        elif result == 'WIN': # return bet and bonus times bet
            bjp.earn((int) (bjp.betAmt * (1+BJBONUS)))
        else: # don't return anything to player
            pass

    def stop(self):
        if not self.playing:
            print("Bet for new round first. [stop called]")
            return False
        # dealer play
        self.dealer.addCards()
        # dealer maintain bet
        self.__collectMoney(self.player)
        self.playing = False
        if self.splitting: self.__splitStop()
        return True

    def doubleMore(self):
        if not self.playing:
            print("Bet for new round first. [doubleMore called]")
            return False

        if self.player.total() >21:
            print("Already exceed 21 [doubleMore called]")
            return False

        if self.player.doubleBet(): # if enough money for doubleBet, spend it and return True
            c = Card(self.dealer.draw())
            self.player.addCard(c)
            self.stop()
            return True

        else:
            print("Not enough money to double. [doubleMore called]")
            return False

    def split(self):
        """If player successfully split the hand, Create another player called splitPlayer"""
        if not self.playing:
            print("Bet for new round first. [split called]")
            return False

        card = self.player.splitHand()

        if card is not None: # if split is legal
            self.splitPlayer = BJSplit(self.player.betAmt, card)
            self.splitting = True
            c1 = Card(self.dealer.draw())
            c2 = Card(self.dealer.draw())
            self.splitPlayer.addCard(c1)
            self.player.addCard(c2)
            return True

        return False

    def splitMoreCard(self):
        if not self.splitting:
            return False
        if self.splitPlayer.total() >21:
            print("Already exceed 21 [splitMoreCard called]")
            return False

        else:
            c = Card(self.dealer.draw())
            self.splitPlayer.addCard(c)
            return True

    def splitDoubleMore(self):
        if not self.splitting:
            return False

        if self.splitPlayer.total() >21:
            print("Already exceed 21 [splitDoubleMore called]")
            return False

        if self.splitPlayer.doubleBet(self.player.cashRemain()):
            self.player.bet(self.player.betAmt)
            c = Card(self.dealer.draw())
            self.splitPlayer.addCard(c)
            self.doneSplitHand = True
            return True

        else:
            print("Not enough money to double. [splitDoubleMore called]")
            return False

    def __splitStop(self):
        """when player done playing split set and original set, call this function"""
        self.__collectMoney(self.splitPlayer)
        self.player.earn(self.splitPlayer.endSplit())
        self.splitting = False
        self.doneSplitHand = True

    def print(self, result = False):
        if self.splitting or self.doneSplitHand:
            self.splitPlayer.showHand()
        self.player.showHand()
        self.dealer.showHand(result)
        if result:
            print("You", self.dealer.judge(self.player))
            print("Cash Remain:", self.player.cashRemain())
        print("--------------------------------------------------------")

class NavigationBar():
    def __init__(self):
        self.betBar = 'Bet and start:'
        self.firstBar = '1 Give up\t2 Split\t3 MoreCard\t4 Double\t5 Stop\nchoose: '
        self.splitBar = 'For split set\n1 MoreCard\t2 Stop\nchoose:'
        self.originBar= 'For original set\n1 MoreCard\t2 Stop\nchoose:'
        self.normalBar= '1 MoreCard\t2 Stop\nchoose:'
        self.infoBar = 'Cash Remain:'

    def showInfo(self, game:BJGameMove):
        print(self.infoBar, game.player.cashRemain())

    def startBet(self, game: BJGameMove):
        """
        If properly bet an amount and start a round, return True
        Otherwise, return False
        """
        while True:
            betAmt = int(input(self.betBar))
            if betAmt>0 and game.newGame(betAmt):
                return True
            elif betAmt<=0:
                return False
            else:
                continue

    def firstChoice(self, game: BJGameMove):
        """Offer GiveUp, Split(if legal), MoreCard, Double, and Stop"""
        while True:
            choose = input(self.firstBar)
            if choose == '1':
                game.giveUp()
                return 'end'
            elif choose == '2':
                if game.split():
                    break
            elif choose == '3':
                game.moreCard()
                break
            elif choose == '4':
                if game.doubleMore():
                    game.stop()
                    return 'end'
            elif choose == '5':
                game.stop()
                return 'end'
            else:
                continue

    def splitChoice(self, game: BJGameMove):
        while True:
            choose = input(self.splitBar)
            if choose == '1':
                if game.splitMoreCard():
                    break
            # elif choose == '2':
            #     if game.splitDoubleMore():
            #         return 'done'
            elif choose == '2':
                return 'done'
            else:
                continue

    def originChoice(self, game: BJGameMove):
        while True:
            choose = input(self.originBar)
            if choose == '1':
                if game.moreCard():
                    break
            # elif choose == '2':
            #     if game.doubleMore():
            #         game.stop()
            #         return 'done'
            elif choose == '2':
                game.stop()
                return 'done'
            else:
                continue

    def normalChoice(self, game: BJGameMove):
        while True:
            choose = input(self.normalBar)
            if choose == '1':
                if game.moreCard():
                    break
            # elif choose == '2':
            #     if game.doubleMore():
            #         game.stop()
            #         return 'done'
            elif choose == '2':
                game.stop()
                return 'done'
            else:
                continue

    def quit(self, game: BJGameMove):
        quit = input('Leave? [y/n] : ')
        if quit == 'y':
            print("You played:",game.player.round,"rounds.")
            return True
        return False

class BJGame():
    def __init__(self, initCapital, nDeck, seed):
        rn.seed(seed)
        self.dealer = BJDealer(nDeck)
        self.player = BJPlayer(initCapital)
        self.game = BJGameMove(self.player, self.dealer)

    def gameStart(self):
        gameOver = False
        bar = NavigationBar()
        bar.showInfo(self.game)
        if not bar.startBet(self.game):
            return
        while not gameOver:
            # bet and start a new round
            self.game.print()
            # choose to GiveUp/Split/MoreCard
            if bar.firstChoice(self.game) is not 'end':
                self.game.print()
                if self.game.splitting:
                    # do split choice first
                    while bar.splitChoice(self.game) is not 'done':
                        self.game.print()
                        continue
                    # do original choice until end of this round
                    self.game.print()
                    while bar.originChoice(self.game) is not 'done':
                        self.game.print()
                        continue
                    self.game.print(result=True)

                else:
                    # do normal choice until end of this round
                    while bar.normalChoice(self.game) is not 'done':
                        self.game.print()
                        continue
                    self.game.print(result=True)
            else:
                self.game.print(result=True)
            bar.showInfo(self.game)
            gameOver = not bar.startBet(self.game)
        print("You played:", self.game.player.round, "rounds.")
############
# BlackJackGame = BJGame(5000, 1, 17)
# # #
# BlackJackGame.gameStart()
