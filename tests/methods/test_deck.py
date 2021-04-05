from methods import Deck
import pytest


@pytest.fixture(scope="module")
def deck():
    deck = Deck()
    return deck


def test_deck(deck):
    assert len(deck.deck) == 52


def test_deck_deal(deck):
    cards = [deck.deal() for _ in range(5)]
    assert len(cards) == 5


def test_recreate_deck(deck):
    cards = [deck.deal() for _ in range(5)]
    new_deck = deck.recreate_deck(cards=cards)
    assert len(new_deck.deck) == 47
    assert all(card not in new_deck.deck for card in cards)
