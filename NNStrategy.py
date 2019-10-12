from sklearn.externals import joblib
import pickle
import pandas as pd
from BJDealer import BJDealer
from BJPlayer import BJPlayer
from BJGame import BJGameMove
from nn_data_generator import KnownCards, CanSplitHand, FaceOfCard

nn = joblib.load('nn_player.pkl')

with open('keras_model_none_split.pkl', 'rb') as f:
    nn_none_split = pickle.load(f)

with open('keras_model_split.pkl', 'rb') as f:
    nn_split = pickle.load(f)

with open('keras_model_features_types.pkl', 'rb') as f:
    nn_feature_types = pickle.load(f)

def prepareFeatures(arr):
    out = pd.DataFrame(columns=nn_feature_types.keys().tolist())
    out.loc[0] = arr
    return out.astype(nn_feature_types)

def nextMove(features, canSplit):
    if canSplit:
        return nn_split.predict_classes(prepareFeatures(features))[0]+1
    move =  nn_none_split.predict_classes(prepareFeatures(features))[0]
    if move == 3:
        return 5
    return move+1

class NNStrategy():
    def __init__(self, initCapital, betPercent, round, pause=False, nDeck=1):
        self.player = BJPlayer(initCapital)
        self.dealer = BJDealer(nDeck)
        self.game = BJGameMove(self.player, self.dealer)
        self.bet = int(initCapital * betPercent)
        self.nRound = round
        self.pauseEachRound = pause
        self.playerMemory = KnownCards()

    def prepareFeature(self):
        features = []
        # features.append(self.playerMemory.nCard)
        features.append(self.playerMemory.nTen)
        # features.append(self.playerMemory.nOne)
        # features.append(self.playerMemory.nAce)
        features.append(self.player.minPoint)
        features.append(self.player.maxPoint)
        features.append(1 if len(self.player.hand)==2 else 0)
        # features.append(CanSplitHand(self.player))
        # features.append(FaceOfCard(self.dealer.hand[0]))
        features.append(self.dealer.nDeck)
        features.append(
            (16*self.dealer.nDeck - self.playerMemory.nTen) / (52*self.dealer.nDeck - self.playerMemory.nCard))
        features.append(
            (4 * self.dealer.nDeck - self.playerMemory.nAce) / (52 * self.dealer.nDeck - self.playerMemory.nCard))
        features.append(
            (32 * self.dealer.nDeck - self.playerMemory.nOne) / (52 * self.dealer.nDeck - self.playerMemory.nCard))
        features.append(FaceOfCard(self.dealer.hand[0]) > 9)
        return features

    def doCoach(self, game:BJGameMove):
        move = nextMove(self.prepareFeature(), CanSplitHand(self.player))
        if move == 1:  # more card
            # print("\n\tMORE\n")
            result = game.moreCard()
            self.playerMemory.add(self.player.hand[-1])
            return result

        elif move == 2: # stop
            # print("\n\tSTOP\n")
            result = game.stop()
            for card in self.dealer.hand[1:]:
                self.playerMemory.add(card)
            return result

        elif move == 3: # double
            # print("\n\tDOUBLE\n")
            result = game.doubleMore()
            self.playerMemory.add(self.player.hand[-1])
            for card in self.dealer.hand[1:]:
                self.playerMemory.add(card)
            return result

        elif move == 4: # split
            # print("\n\tSPLIT\n")
            result = game.split()
            self.playerMemory.add(self.player.hand[-1])
            self.playerMemory.add(self.game.splitPlayer.hand[-1])
            return result

        elif move == 5: # give up
            # print("\n\tGIVEUP\n")
            result = game.giveUp()
            for card in self.dealer.hand[1:]:
                self.playerMemory.add(card)
            return result

        else:
            return False

    def doCoachAtSplit(self, game:BJGameMove):
        feature = self.prepareFeature()
        feature[6] = 0
        feature[7] = 0
        move = nextMove(feature)
        if move == 1:
            # print("\n\t(SPLIT) MORE\n")
            result = game.moreCard()
            self.playerMemory.add(self.player.hand[-1])
            return result

        elif move == 2:
            # print("\n\t(SPLIT) STOP\n")
            result = game.stop()
            for card in self.dealer.hand[1:]:
                self.playerMemory.add(card)
            self.game.doneSplitHand = True
            return result

        elif move == 3:
            # print("\n\t(SPLIT) DOUBLE\n")
            result = game.splitDoubleMore()
            self.playerMemory.add(self.player.hand[-1])
            for card in self.dealer.hand[1:]:
                self.playerMemory.add(card)
            return result

        else:
            return False

    def nextStep(self, game):
        if self.game.splitting:
            if not self.game.doneSplitHand:
                return self.doCoachAtSplit(game)
            else:
                return self.doCoach(game)
        else:
            return self.doCoach(game)

    def play(self, showGame = False):
        while self.player.round < self.nRound or self.game.playing:
            if not self.game.playing:
                if self.dealer.cardLeft < 17 * self.dealer.nDeck:
                    self.playerMemory.reset()
                start_new_game = self.game.newGame(self.bet)
                self.playerMemory.add(self.dealer.hand[0])
                self.playerMemory.add(self.player.hand[0])
                self.playerMemory.add(self.player.hand[1])
                if not start_new_game: # can't start newGame -> End
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
# import numpy.random as rn
# test = NNStrategy(5000,0.02,100,pause=False, nDeck=6)
# rn.seed(999)
# test.play(showGame=False)
################
