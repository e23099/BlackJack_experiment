from RandomStrategy import RandomStrategy
from DealerStrategy import DealerStrategy
from BasicStrategy import BasicStrategy

import numpy.random as rn

DECK = 6
TESTAMT = 5000
ROUND   = 100
BETRATIO= 0.02
N = 10
SEED = 127

rn.seed(SEED)

print("seed = %d\nnDeck =  %d \ninitCapital = %d\nbetRatio = %.2f\nround = %d\n" % (SEED, DECK, TESTAMT, BETRATIO, ROUND))

print("========== Basic Strategy ==========")
for game in range(N):
    test = BasicStrategy(TESTAMT, BETRATIO, ROUND, pause=False, nDeck= DECK)
    test.play(showGame = False)

print("\n\n========== Dealer Strategy ==========")
for game2 in range(N):
    test = DealerStrategy(TESTAMT, BETRATIO, ROUND, pause=False, nDeck= DECK)
    test.play()

print("\n\n========== Random Strategy ==========")
for game3 in range(N):
    test = RandomStrategy(TESTAMT, BETRATIO, ROUND, pause=False, nDeck= DECK)
    test.play()