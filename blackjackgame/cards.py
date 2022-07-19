#! /usr/bin/env python3
# Joseph Nasr
# CPSC 386-01
# 2022-04-04
# jenasr@csu.fullerton.edu
# @jenasr
#
# Lab 03-00
#
# File for Cards
#
"""For the Cards in Black Jack"""

from collections import namedtuple
from random import shuffle, randrange
from math import floor
from .functions import printt

# class premade for us.
# you can adjust this to your taste!
Card = namedtuple("Card", ["rank", "suit"])
# Name of the struct I want; use rank, suit


def reshuffle():
    """Make a new deck"""
    printt("We must shuffle the deck")
    new_deck = Deck(60, 80)
    for i in range(7):
        printt(i + 1)
        new_deck.merge(Deck())
        new_deck.shuffle()
    new_deck.cut()
    return new_deck


def stringify_card(card):
    """Allows a card to be in printable string format"""
    return f"{card.rank}{card.suit}"


Card.__str__ = stringify_card
# set the str method to what stringify_card does
# the first parameter c gets the self of Card as its argument
Card.__repr__ = stringify_card


def card_value(card):
    """Get value of card"""
    return Deck.values_dict[(card.rank)]


class Deck:
    """A deck object for a collection of cards"""

    ranks = ["Ace"] + [str(x) for x in range(2, 11)] + "Jack Queen King".split()
    suits = "\u2663 \u2660 \u2666 \u2665".split()
    # values =  list(range(1,11) + [10,10,10])
    values = list(range(1, 11)) + [10, 10, 10]
    values_dict = dict(zip(ranks, values))

    def __init__(self, cut_card_position_min=0, cut_card_position_max=0):
        """Deck Initializer"""
        self._cards = [
            Card(rank, suit) for suit in self.suits for rank in self.ranks
        ]
        if cut_card_position_min == 0 and cut_card_position_max == 0:
            self._cut_card_position = 10
        else:
            self._cut_card_position = randrange(
                cut_card_position_min, cut_card_position_max + 1
            )
        self._reached = False
        self._cards_dealt = 0

    @property
    def reached(self):
        """Reached Getter"""
        return self._reached

    @reached.setter
    def reached(self, value):
        """Reached setter"""
        self._reached = value

    def set_cut_card_position(self, min_p, max_p):
        """Resets cut card position"""
        self._cut_card_position = randrange(min_p, max_p)

    def needs_shuffle(self):
        """Checks if the deck needs to be shuffled"""
        return self._cards_dealt == self._cut_card_position

    def __getitem__(self, position):
        """Get the items position"""
        return self._cards[position]

    def __len__(self):
        """Get the length of the deck"""
        return len(self._cards)

    def shuffle(self, number=1, out=1):
        """Shuffle the deck n number of times"""
        if out:
            printt("Shuffling")
        for _ in range(number):
            shuffle(self._cards)

    def cut(self):
        """Perform a cut of the deck"""
        printt("Cutting")
        bound = floor(len(self._cards) * 0.2)
        half = len(self._cards) // 2 + randrange(-bound, bound)
        # 2 slashes is integer arithmetic
        tophalf = self._cards[:half]
        bottomhalf = self._cards[half:]
        self._cards = bottomhalf + tophalf

    def __str__(self):
        """Print out the cards of the deck"""
        return "\n".join(map(str, self._cards))

    def merge(self, other_deck):
        """Puts 2 decks together"""
        self._cards += other_deck.cards
        # d.merge(Deck())

    def deal(self, number=1):
        """Deal n number of cards to a player"""
        card = [self._cards.pop(0) for _ in range(number)]
        # printt(f"Deal card: {card[0]}")
        self._cards_dealt += 1
        if self.needs_shuffle() and not self._reached:
            printt("The Cut Card has been reached")
            self._reached = True
        return card

    @property
    def cards(self):
        """Cards Getter"""
        return self._cards

    Card.__int__ = card_value
