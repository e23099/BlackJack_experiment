from BJDealer import BJDealer
from BJPlayer import BJPlayer
from BJGame import BJGameMove
from numpy import random as rn

class DealerStrategy():
    def __init__(self, initCapital, betPercent, round, pause = False, nDeck = 1):
        self.player = BJPlayer(initCapital)
        self.dealer = BJDealer(nDeck)
        self.game = BJGameMove(self.player, self.dealer)
        self.bet = int(initCapital * betPercent)
        self.nRound = round
        self.pauseEachRound = pause

    def nextStep(self, game: BJGameMove):
        if game.player.total() < 17:
            return game.moreCard()
        if game.player.total() >= 17:
            return game.stop()

    def play(self, showGame = False):
        while self.player.round < self.nRound or self.game.playing:
            if not self.game.playing:
                if not self.game.newGame(self.bet): # can't start newGame -> End
                    print("can't start new round")
                    break

            if not self.nextStep(self.game): # playing but can't start nextStep -> End
                print("next step failed.")
                break

            if self.game.playing:
                if showGame:
                    self.game.print()
            else:
                if showGame:
                    self.game.print(result=True)

            if self.pauseEachRound:
                input("Press any key to continue...")
        self.endPlay()

    def endPlay(self):
        print(self.player.cashRemain(), "dollar left.\tYou played",
              self.player.round,"rounds.")

###########
# test = DealerStrategy(5000, 0.02, 100, pause=False)
# rn.seed(121)
# test.play(showGame=True)