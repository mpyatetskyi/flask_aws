from enum import Enum, IntEnum
from random import shuffle
from dataclasses import dataclass, asdict
from dataclasses_json import dataclass_json
import json


class Suits(IntEnum):
    HEARTS = 1
    DIAMONDS = 2
    SPADES = 3
    CLUBS = 4


class Ranks(IntEnum):
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12
    ACE = 13

@dataclass_json
@dataclass(frozen=True)
class Card:
    suit: Suits
    rank: Ranks

    def to_id(self, card):
        return card.suit.value * 100 + card.rank.value

    @staticmethod
    def from_id(id):
        suit = Suits(id // 100)
        rank = Ranks(id % 100)
        return Card(suit, rank)

    def __repr__(self):
        return f'({self.rank.name}, {self.suit.name})'


#card = Card(Suits.HEARTS, Ranks.ACE)
#card1 = Card(Suits.SPADES, Ranks.JACK)
#print(card.to_id(card))
#print(card.to_id(card1))

#print(Card.from_id(213).to_json())
#print(asdict(Card(Suits.HEARTS, Ranks.ACE)))

#rint(asdict(Card(Suits.HEARTS, Ranks.ACE)).items())


#print(asdict(card))
#print(card)

#card = Card(Suits.HEARTS, Ranks.ACE)
#print(card)
#card_json = card.to_json()
#print(card_json)
#c = Card.from_json(card_json)
#print(c)



class Deck:

    def __init__(self):
        self.deck = [Card(s, r) for s in Suits for r in Ranks]

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.rank + card.suit()
        return "The deck has: " + deck_comp

    def shuffle(self):
        shuffle(self.deck)

    def deal(self):
        if len(self.deck) > 1:
            return self.deck.pop()


def card_id(card):
    return card.suit.value*100 + card.rank.value


def from_id(id):
        suit = Suits(id // 100)
        rank = Ranks(id % 100)
        return Card(suit, rank)


@dataclass_json
@dataclass(frozen=True)
class GameDataDTO:
    game_id: int
    cards: list
    status: bool




