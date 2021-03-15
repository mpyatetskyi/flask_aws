from methods import Card, Status, Suits, Ranks, Deck


def test_cards_value():
    aces_2 = [Card(Suits.SPADES, Ranks.ACE),
              Card(Suits.DIAMONDS, Ranks.ACE)]
    aces_3 = [Card(Suits.SPADES, Ranks.ACE),
              Card(Suits.DIAMONDS, Ranks.ACE),
              Card(Suits.HEARTS, Ranks.ACE)]
    aces_4 = [Card(Suits.SPADES, Ranks.ACE),
              Card(Suits.DIAMONDS, Ranks.ACE),
              Card(Suits.HEARTS, Ranks.ACE),
              Card(Suits.CLUBS, Ranks.ACE)]
    jack_2 = [Card(Suits.SPADES, Ranks.JACK),
              Card(Suits.DIAMONDS, Ranks.JACK)]
    jack_3 = [Card(Suits.SPADES, Ranks.JACK),
              Card(Suits.DIAMONDS, Ranks.JACK),
              Card(Suits.HEARTS, Ranks.JACK)]
    jack_4 = [Card(Suits.SPADES, Ranks.JACK),
              Card(Suits.DIAMONDS, Ranks.JACK),
              Card(Suits.HEARTS, Ranks.JACK),
              Card(Suits.CLUBS, Ranks.JACK)]
    two_three = [Card(Suits.SPADES, Ranks.TWO),
                 Card(Suits.DIAMONDS, Ranks.THREE)]
    ace_2king = [Card(Suits.SPADES, Ranks.KING),
                 Card(Suits.DIAMONDS, Ranks.ACE),
                 Card(Suits.HEARTS, Ranks.KING)]
    deck = Deck()

    assert Status.cards_value(aces_2) == 12
    assert Status.cards_value(aces_3) == 13
    assert Status.cards_value(aces_4) == 14
    assert Status.cards_value(jack_2) == 20
    assert Status.cards_value(jack_3) == 30
    assert Status.cards_value(jack_4) == 40
    assert Status.cards_value(two_three) == 5
    assert Status.cards_value(deck.deck) == 340
    assert Status.cards_value(ace_2king) == 21


def test_status_player_only():
    win = [Card(Suits.SPADES, Ranks.KING),
           Card(Suits.DIAMONDS, Ranks.ACE)]
    loose = [Card(Suits.SPADES, Ranks.KING),
             Card(Suits.DIAMONDS, Ranks.ACE),
             Card(Suits.HEARTS, Ranks.KING),
             Card(Suits.SPADES, Ranks.TWO)]
    go_on = [Card(Suits.SPADES, Ranks.TWO),
             Card(Suits.DIAMONDS, Ranks.THREE)]
    target_20 = [Card(Suits.SPADES, Ranks.KING),
                 Card(Suits.HEARTS, Ranks.KING)]

    assert Status.status_check(win) is True
    assert Status.status_check(loose) is False
    assert Status.status_check(go_on) is None
    assert Status.status_check(win, dealer_value=go_on) is True
    assert Status.status_check(win, dealer_value=win) is None
    assert Status.status_check(go_on, dealer_value=win) is False
    assert Status.status_check(target_20, dealer_value=go_on) is True

