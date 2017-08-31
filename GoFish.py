import random
# this project was adapted from these projects:
# https://rosettacode.org/wiki/Go_Fish/Python
# https://github.com/alyssadmoore/Capstone_Project_1/tree/master/PycharmProjects/Project1
# https://www.youtube.com/watch?v=fBQGrtVxiUQ&t=736s

# creates a card object with suit and rank
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

# to string def statement
    def __str__(self):
        return "%s of %s" % (self.rank, self.suit)

# creates a deck class object which builds a deck of card objects
class Deck:
    def __init__(self):
        self.deck = []
        self.rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.suit = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
# builds deck
        for s in self.suit:
            for r in self.rank:
                self.deck.append(Card(r, s))
# shuffle deck
        random.shuffle(self.deck)
# draw card def statement

    def drawCard(self):
        drawnCard = self.deck.pop()
        return drawnCard

name = input("Please enter player name...: ")

# player class
class PlayerOne:
    def __init__(self):

        self.score = 0
        self.pairs = []
        self.hand = []

        min_hand = 0
        max_hand = 7
# initializes hand to 7 cards
        while min_hand < max_hand:
            self.hand.append(Deck().drawCard())
            min_hand += 1
# shows hand
    def showHand(self):
        for card in self.hand:
            print(card.__str__())

# request a card as long as you name a card in your hand
    def request(self):
        while True:
            request = input("What rank would you like to ask for?\n")
            choice = []
            for card in self.hand:
                if card.rank == request:
                    choice.append(card.rank)
                    break
            if len(choice) == 0:
                print("You can only ask for cards in your hand. Please try again.")
            else:
                break
        return request
# turn method checks if cards are in hand, then uses request to ask computer for card
# if you ask for the right card the computer hands it over, otherwise you draw a card
    def turn(self):

        self.showHand()

        if len(self.hand) != 0:
            request = self.request()
            requested = []

            for card in Computer().handComp:
                if card.rank == request:
                    requested.append(card)

            for card in requested:
                self.hand.append(card)
                Computer().handComp.remove(card)
                print("Computer gave you " + card.__str__(card) + ".")

            if len(requested) == 0:
                print("Go Fish!")
                Deck().drawCard()
                self.showHand()

            if checkMatch(self.hand):
                self.score += 1
                self.showHand()
                checkForWin()

        if len(Deck().deck) != 0 and len(self.hand) == 0:
            card = Deck().drawCard()
            self.hand.append(card)

#computer class, initializes the computer hand
class Computer:
    def __init__(self):
        self.name = 'Computer'
        self.score = 0
        self.pairsComp = []
        self.handComp = []

        min_hand = 0
        max_hand = 7

        while min_hand < max_hand:
            self.handComp.append(Deck().drawCard())
            min_hand += 1

# computers turn, makes a random guess from its hand. AI will be to further develop to remember
# cards that player asked if computer ends up drawing the card

    def comp_turn(self):
        random.shuffle(self.handComp)
        guess = 1

        if len(self.handComp) == 0 and len(Deck().deck) != 0:
            self.handComp.append(Deck().drawCard())

        if (len(self.handComp) == 0 or len(PlayerOne().hand) == 0) and len(Deck().deck) == 0:

            if checkMatch(self.handComp):
                self.score += 1
            else:
                for card in self.handComp:
                    guess = card.rank

        if guess != 1:

            print("Computer asks if you have any " + str(guess) + ".")
            requested = []

            for card in PlayerOne().hand:
                if card.rank == str(guess):
                    requested.append(card)

            for card in requested:
                self.handComp.append(card)
                PlayerOne().hand.remove(card)
                print("You gave the computer " + card.__str__(card) + ".")

            if len(requested) == 0:
                print("The computer goes fishing...")
                self.handComp.append(Deck().drawCard())

            if checkMatch(self.handComp):
                self.score += 1
                checkForWin()

# checks for pairs of cards in hands
def checkMatch(hand):
    for card in hand:
        pairs = []
        rank = card.rank
        suit = card.suit

        for x in hand:
            if x.rank == rank and x.suit != suit:
                pairs.append(x)
        if len(pairs) == 1:
            hand.remove(card)
            hand.remove(pairs[0])
            return True
# checks for winning conditions, if deck runs out measures the pairs between computer and player
def checkForWin():
    if len(Deck().deck) == 0:
        if len(Computer().pairsComp) > len(PlayerOne().pairs):
            print("Computer Wins")
        if len(Computer().pairsComp) < len(PlayerOne().pairs):
            print(name + " Wins!")
        return True

while True:

    PlayerOne().turn()
    if checkForWin():
        break

    Computer().comp_turn()
    if checkForWin():
        break



