from random import shuffle


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit


class Deck:
    def __init__(self, shuffled=True):
        self.state = list()
        for suit in range(4):
            for value in range(13):
                self.state.append(Card(value, suit))
        if shuffled:
            self.shuffle()

    def shuffle(self):
        shuffle(self.state)

    def draw(self):
        return self.state.pop(-1)

    def add(self, card):
        if type(card) is Card:
            self.state.append(card)
        else:
            raise Exception("Can't add non-card object")
