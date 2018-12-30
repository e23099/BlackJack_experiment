###
# RandomStrategy is base on a fixed table containing situations for which each hand should play.
# According to this table, the player will choose randomly from 6 actions:
# 0: do nothing
# 1: more card
# 2: double
# 3: stop
# 4: split
# 5: give up
###

from BJDealer import BJDealer
from BJPlayer import BJPlayer
from BJGame import BJGameMove
from numpy import random as rn

class RandomStrategy():
    def __init__(self, initCapital, betPercent, round, pause = False, nDeck = 1):
        self.player = BJPlayer(initCapital)
        self.dealer = BJDealer(nDeck)
        self.game = BJGameMove(self.player, self.dealer)
        self.bet = int(initCapital * betPercent)
        self.nRound = round
        self.pauseEachRound = pause
        self.FirstChoice = {
            'A1':[4],       'A2':[1],       'A3':[1,3,5],   'A4':[1,3,5], 'A5':[1,3,5],
            'A6':[1,3,5],   'A7':[1,3],     'A8':[1,2,3],   'A9':[1,2,3], 'AX':[3],
            '77':[1,3,4,5], '88':[1,3,4,5], '4' :[1],       '5' :[1],     '6' :[1],
            '7' :[1],       '8' :[1],       '9' :[1,2],     '10':[1,2],   '11':[1,2],
            '12':[1],       '13':[1],       '14':[1,3,5],   '15':[1,3,5], '16':[1,3,5],
            '17':[1,3,5],   '18':[3],       '19':[3],       '20':[3],     '21':[0],
            'XX':[3]
        }
        self.SecondChoice = {
            'A1': [1],      'A2': [1],     'A3': [1, 3],    'A4': [1, 3],    'A5': [1, 3],
            'A6': [1, 3],   'A7': [1, 3],  'A8': [1, 3],    'A9': [1, 3],    'AX': [3],
            '77': [0],      '88': [0],     '4' : [0],       '5' : [0],       '6' : [1],
            '7' : [1],      '8' : [1],     '9' : [1],       '10': [1],       '11': [1],
            '12': [1],      '13': [1],     '14': [1, 3],    '15': [1, 3],    '16': [1, 3],
            '17': [1, 3],   '18': [3],     '19': [3],       '20': [3],       '21': [3],
            'XX': [3]
        }

    def deriveHand(self, player: BJPlayer):
        """
        derive hand cards and interpret them into face of hand
        return face of hand (in the form of 'XX')
        """
        # case0 : exceed 21
        if player.minPoint > 21:
            return 'XX'
        # case1 : at least an Ace in hand
        if player.maxPoint != player.minPoint:
            if player.total() > 21:
                return 'A' + str(player.minPoint - 1)
            elif player.total() == 21:
                if len(player.hand) == 2:
                    return 'AX'
                return '21'
            elif player.minPoint < 11:
                return 'A' + str(player.minPoint -1)
            else:
                return str(player.total())
        else:
            # case2 : 77 or 88
            if player.hand[0].face == player.hand[1].face and player.hand[0].face in [6, 7]:
                if len(player.hand) == 2:
                    return '77' if player.hand[0].face == 6 else '88'
            # case3 : not 77 or 88 and no Ace in hand
            else:
                return str(player.minPoint)

    def coach(self, hand, isFirstChoice):
        """
        Base on hand and isFirstChoice,
        tell the according choice.

        return 1 ~ 5 representing the chose option
        return 0 when no option is chosen
        """
        if isFirstChoice:
            return int(rn.choice(self.FirstChoice[hand]))
        else:
            return int(rn.choice(self.SecondChoice[hand]))

    def doCoach(self, option, game: BJGameMove):
        """
        receive an option from coach, and actually do it
        if success, return True
        else, return False
        """
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
            game.splitMoreCard()

        elif option == 7: # split double
            print("(split) double")
            game.splitDoubleMore()

        elif option == 8: # split stop
            print("(split) stop")
            self.game.doneSplitHand = True
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
                self.doCoach(splitChoice+5, game) # small trick: +5 indicates split choices

            choice = self.coach(hand, False)
            return self.doCoach(choice, game)

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
                input("Press any key to continue...")
        self.endPlay()

    def endPlay(self):
        print(self.player.cashRemain(), "dollar left.\tYou played",
              self.player.round,"rounds.")


################
# import time
# t1 = time.time()
# rsGame = RandomStrategy(5000, 0.05, 100, pause=True)
# rn.seed(121)
# rsGame.play(showGame=True)
# print("take",time.time() - t1 , 's')
