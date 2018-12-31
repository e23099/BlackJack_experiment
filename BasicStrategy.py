from BJDealer import BJDealer
from BJPlayer import BJPlayer
from BJGame import BJGameMove

# Note: In the methods of BasicStrategy class,
#       only deriveHand and coach will change from the RandomStrategy class.

class BasicStrategy():
    def __init__(self, initCapital, betPercent, round, pause = False, nDeck = 1):
        self.player = BJPlayer(initCapital)
        self.dealer = BJDealer(nDeck)
        self.game = BJGameMove(self.player, self.dealer)
        self.bet = int(initCapital * betPercent)
        self.nRound = round
        self.pauseEachRound = pause
        self.FirstChoice = {
            # Hard hand
            '5': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 5},
            '6': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 5},
            '7': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 5},
            '8': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '9': {'2': 1, '3': 2, '4': 2, '5': 2, '6': 2, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '10': {'2': 2, '3': 2, '4': 2, '5': 2, '6': 2, '7': 2, '8': 2, '9': 2, 'T': 1, 'A': 1},
            '11': {'2': 2, '3': 2, '4': 2, '5': 2, '6': 2, '7': 2, '8': 2, '9': 2, 'T': 1, 'A': 1},
            '12': {'2': 1, '3': 1, '4': 3, '5': 3, '6': 3, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 5},
            '13': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 5},
            '14': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 1, '8': 1, '9': 1, 'T': 5, 'A': 5},
            '15': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 1, '8': 1, '9': 1, 'T': 5, 'A': 5},
            '16': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 1, '8': 1, '9': 5, 'T': 5, 'A': 5},
            '17': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3, 'T': 3, 'A': 5},
            '18': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3, 'T': 3, 'A': 3},
            # Soft hand
            'A2': {'2': 1, '3': 1, '4': 1, '5': 2, '6': 2, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            'A3': {'2': 1, '3': 1, '4': 1, '5': 2, '6': 2, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            'A4': {'2': 1, '3': 1, '4': 2, '5': 2, '6': 2, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            'A5': {'2': 1, '3': 1, '4': 2, '5': 2, '6': 2, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            'A6': {'2': 1, '3': 2, '4': 2, '5': 2, '6': 2, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            'A7': {'2': 3, '3': 2, '4': 2, '5': 2, '6': 2, '7': 3, '8': 3, '9': 1, 'T': 1, 'A': 1},
            'A8': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3, 'T': 3, 'A': 3},
            'A9': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3, 'T': 3, 'A': 3},
            # Pairs
            '22': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '33': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 1, '9': 1, 'T': 1, 'A': 5},
            '44': {'2': 1, '3': 1, '4': 1, '5': 4, '6': 4, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '55': {'2': 2, '3': 2, '4': 2, '5': 2, '6': 2, '7': 2, '8': 2, '9': 2, 'T': 1, 'A': 1},
            '66': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 5},
            '77': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 1, '9': 1, 'T': 5, 'A': 5},
            '88': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 4, '9': 4, 'T': 5, 'A': 5},
            '99': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 3, '8': 4, '9': 4, 'T': 3, 'A': 3},
            'TT': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3, 'T': 3, 'A': 3},
            'AA': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 4, '9': 4, 'T': 4, 'A': 1},
        }
        self.SecondChoice = {
            # Hard hand
            '5': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '6': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '7': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '8': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '9': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '10': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '11': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '12': {'2': 1, '3': 1, '4': 3, '5': 3, '6': 3, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '13': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '14': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '15': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '16': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '17': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3, 'T': 3, 'A': 3},
            '18': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3, 'T': 3, 'A': 3},
            # Soft hand
            'A2': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            'A3': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            'A4': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            'A5': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            'A6': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            'A7': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 1, 'T': 1, 'A': 1},
            'A8': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3, 'T': 3, 'A': 3},
            'A9': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3, 'T': 3, 'A': 3},
            # Pairs
            '22': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '33': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '44': {'2': 1, '3': 1, '4': 1, '5': 4, '6': 4, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '55': {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '66': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 1, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '77': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 1, '9': 1, 'T': 1, 'A': 1},
            '88': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 4, '9': 4, 'T': 1, 'A': 1},
            '99': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 3, '8': 4, '9': 4, 'T': 3, 'A': 3},
            'TT': {'2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3, 'T': 3, 'A': 3},
            'AA': {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 4, '9': 4, 'T': 4, 'A': 1},
        }

    def deriveHand(self, player: BJPlayer):
        # case0: exceed 21
        if player.total()>21:
            return '18'
        # case1: Pairs
        twoTen = player.hand[0].face >= 9 and player.hand[1].face >= 9
        if player.hand[0].face == player.hand[1].face or twoTen:
            if player.hand[0].face == 0:
                return 'AA'
            if player.hand[0].face >= 9:
                return 'TT'
            return str(11* (player.hand[0].face+1))
        # case2: Soft total
        elif player.minPoint != player.maxPoint and player.minPoint < 11:
            return 'A'+ str(player.minPoint-1)
        # case3: Hard total
        else:
            if player.total() >= 18:
                return '18'
            else:
                return str(player.total())

    def coach(self, hand, isFirstChoice):
        holeCard = self.game.dealer.hand[1].face
        if holeCard == 0:
            hole = 'A'
        elif holeCard >= 9:
            hole = 'T'
        else:
            hole = str(holeCard+1)

        if isFirstChoice:
            return self.FirstChoice[hand][hole]

        return self.SecondChoice[hand][hole]

    def doCoach(self, option, game: BJGameMove):
        if option == 1: # more card
            print("more")
            return game.moreCard()

        elif option == 2: # double more
            print("double")
            return game.doubleMore()

        elif option == 3: # stop
            print("stop")
            return game.stop()

        elif option == 4: # split
            print("split")
            return game.split()

        elif option == 5: # give up
            print("give up")
            return game.giveUp()

        elif option == 6: # split more
            print("(split) more")
            return game.splitMoreCard()

        elif option == 7: # split double
            print("(split) double")
            return game.splitDoubleMore()

        elif option == 8: # split stop
            print("(split) stop")
            self.game.doneSplitHand = True
            return True
        else:
            return False

    def nextStep(self, game: BJGameMove):
        """
        first check if it's first choice (and tell it to Coach)

        base on what the player has in his hand,
        try to do next step according to "Coach"

        if success, return True
        else, return False
        """
        isFirstChoice = len(game.player.hand) == 2 and not game.splitting
        hand = self.deriveHand(game.player)

        if self.game.splitting:
            if not self.game.doneSplitHand:
                splitHand = self.deriveHand(game.splitPlayer)
                splitChoice = self.coach(splitHand, False)
                return self.doCoach(splitChoice+5, game) # small trick: +5 indicates split choices
            else:
                choice = self.coach(hand, False)
                return self.doCoach(choice, game)
        else:
            choice = self.coach(hand, isFirstChoice)
            return self.doCoach(choice, game)

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
                input("Press ENTER to continue...")
        self.endPlay()

    def endPlay(self):
        print(self.player.cashRemain(), "dollar left.\tYou played",
              self.player.round,"rounds.")

################
import numpy.random as rn
test = BasicStrategy(5000,0.02,1000,pause=True)
rn.seed(17)
test.play(showGame=True)
################
