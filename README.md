# BlackJack_experiment
A simulation of playing BlackJack with different strategies

## What is Black Jack?

Black Jack is a poker game in which the player plays against the dealer only. It's popular among casinos around the world, yet the it's rule differs in places.
In our simulation, we only consider some common rules found online, and they're mainly based on the website https://www.blackjackinfo.com/.

In short, rules of black jack game can be devided into three parts: the card, the dealer and the player.

### Cards
There are only 10 kinds of cards:an ace, a ten, and everything between them. A ten contains 10, Jack, Queen, and the King.
Ace can be treated as 1 point or 10 points, the other cards are counted according to their kinds.
On starting the game, player will received two cards from dealer. If they are an ace and a ten, then it is a "Black Jack".

### Dealer
Dealer has a fixed way of playing, which is adding more cards until he/she reaches 17 points in total.

### Player
Player has 5 options to do when playing the game, as shown in the following table.

|option|description|done in first choice| done in second choice|
| --- | --- | --- | --- |
|more card| add one more card| yes| yes|
|double| double the bet and add one more card| yes| no|
|stop| stop and wait for result| yes| yes|
|split| split your first two cards into two set when they are of the same kind| yes| no|
|give up| give up the game and take back half of the bet| yes|no|

By first choice, we mean the first choice after you received the first two cards. After that, every choice is a second choice.

## What is this experiment about?

Inspired by the movie *21*, we want to find out if there is a optimal playing strategy for black jack game. 
Assuming that the player doesn't have to remember the cards, we come up with 3 strategies to play against the dealer.
Given the initial capital for the gambling, and the rounds being played for each strategies,
we want to know at the end, which strategy will stand out from the rest, and on what kind of conditions(like how much to bet?) will the player most
possibliy keep the money.

### Strategy 1: Dealer's Strategy

Simply mimicking how the dealer play the game, will a player benefits from that?

### Strategy 2: Basic Strategy

Applying the so called "Basic Strategy" from blackjackinfo.com, with the rules set accordingly, will the player earns the most? (we hope so)

### Strategy 3: Random Strategy

For comparison, we come up with the idea of randomly choosing the options while playing. As a black jack naive, one may be confident
to make a decision like "more card" or "stop" in some situation, while being totally confused in the other. By defining a "hesitation range"
of total points at hand, and making some assumption, we can conclude the possible options for each possible situation. And hence randomly
choosing from these options forms the strategy.

When choosing hesitation range of total points as 14~17, the options are as follow:
