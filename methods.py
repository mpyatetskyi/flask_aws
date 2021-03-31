from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import IntEnum
from random import shuffle


class Suits(IntEnum):
    HEARTS = 1
    DIAMONDS = 2
    SPADES = 3
    CLUBS = 4


class Ranks(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


@dataclass_json
@dataclass(frozen=True)
class Card:
    suit: Suits
    rank: Ranks

    def to_id(self) -> int:
        """Turns a card object into numeric id
        to store it in database"""
        return self.suit.value * 100 + self.rank.value

    @staticmethod
    def from_id(card_id: int) -> object:
        """Turns a numeric id of a card into
         card object"""
        suit = Suits(card_id // 100)
        rank = Ranks(card_id % 100)
        return Card(suit, rank)

    def __repr__(self):
        return f'({self.rank.name}, {self.suit.name})'


class Deck:

    def __init__(self):
        self.deck = [Card(s, r) for s in Suits for r in Ranks]
        shuffle(self.deck)

    def deal(self):
        """Deals one card from a deck"""
        if len(self.deck) > 1:
            return self.deck.pop()

    @staticmethod
    def recreate_deck(cards: list[object]) -> object:
        """Recreates deck of cards without cards that
        are on dealer and """
        deck = Deck()
        for card in cards:
            deck.deck.remove(card)
        return deck


class Status:

    def __init__(self):
        pass

    @staticmethod
    def cards_value(cards: list[Card]) -> int:
        if len(cards) <= 1:
            return 0
        aces = 0
        value = 0
        for card in cards:
            if card.rank.name == 'ACE':
                value += 11
                aces += 1
            elif card.rank.name in ['JACK', 'QUEEN', 'KING']:
                value += 10
            else:
                value += card.rank.value
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    @staticmethod
    def status_check(user_value,
                     dealer_value=[]):
        user = Status.cards_value(user_value)
        if dealer_value == []:
            if user < 21:
                return None
            elif user == 21:
                return True
            else:
                return False
        else:
            dealer = Status.cards_value(dealer_value)
            if user == dealer:
                return None
            elif dealer == 21:
                return False
            elif dealer > 21:
                return True
            elif user > dealer:
                return True
            elif user < dealer:
                return False
