#! /usr/bin/env python3
# Joseph Nasr
# CPSC 386-01
# 2022-04-04
# jenasr@csu.fullerton.edu
# @jenasr
#
# Lab 03-00
#
# File for Player
#
"""For the Players of Black Jack"""
from .functions import printt


def hand_sum(curr_hand):
    """Calculates the sum of a hand"""
    total = sum(map(int, curr_hand))
    if sum(map(lambda c: c.rank == "Ace", curr_hand)) and total + 10 <= 21:
        total += 10
    return total


class Player:
    """Player Object"""

    def __init__(self, name, bankroll=10000.00):
        """Player Initializer"""
        self._name = name
        self._balance = bankroll
        self._bet = []
        self._side_bet = 0
        self._hand = []

    @property
    def name(self):
        """Name Getter"""
        return self._name

    @property
    def balance(self):
        """Balance Getter"""
        return self._balance

    @balance.setter
    def balance(self, value):
        """Balance Setter"""
        self._balance = value

    @property
    def bet(self):
        """Bet Getter"""
        return self._bet

    @property
    def side_bet(self):
        """Side Bet Getter"""
        return self._side_bet

    @property
    def hand(self):
        """Hand Getter"""
        return self._hand

    @hand.setter
    def hand(self, empty):
        """Used for hand reseting"""
        self._hand = empty

    @side_bet.setter
    def side_bet(self, value):
        """Side Bet Setter"""
        self._side_bet = value

    def rev_hand(self, hand):
        """Reveal the players hand"""
        printt("-" * 50)
        printt(f"{self._name}, your hand:")
        printt(str([card for card in hand])[1:-1])
        printt(f"Hand value: {hand_sum(hand)}")

    def does_split(self):
        """Ask Player if they want to split"""
        if self.balance == 0 or self.balance - self._bet[0] < 0:
            return False
        printt("-" * 50)
        resp = input(f"{self._name} do you want to split? ")
        return resp in ("y", "Y")

    def does_double_down(self, curr):
        """Ask Player if they want to double down"""
        if self.balance == 0 or self.balance - self._bet[curr] < 0:
            return False
        printt("-" * 50)
        resp = input(f"{self._name} do you want to double down? ")
        return resp in ("y", "Y")

    def does_hit(self):
        """Ask Player if they want hit"""
        printt("-" * 50)
        resp = input(f"{self._name} do you want to hit? ")
        return resp in ("y", "Y")

    def buys_insurance(self):
        """Checks if player wants to buy insurance"""
        if self.balance == 0:
            return False
        printt("-" * 50)
        resp = input(f"{self.name}, would you like to buy insurance? ")
        return resp in ("y", "Y")

    def has_split(self):
        """Checks if a player splits hand"""
        return len(self._hand) > 1

    def has_bust(self, curr_hand, ind=False):
        """Check if player has busted"""
        if hand_sum(curr_hand) > 21:
            if not ind:
                printt(f"{self.name}, you have Busted")
            return True
        if not ind:
            printt(f"{self.name}, you have not Busted")
        return False

    def black_jack(self, curr_hand):
        """Check if player has blackjack"""
        if hand_sum(curr_hand) == 21:
            return True
        return False

    def has_21(self, curr_hand):
        """Check if player has blackjack"""
        if hand_sum(curr_hand) == 21:
            printt(f"{self.name}, you have 21!")
            return True
        return False

    def perform_split(self, blja):
        """Splits player hand"""
        sec_hand = []
        sec_hand.append(self.hand[0].pop())
        self.hand.append(sec_hand)
        self.hand[0].append(blja.deal()[0])
        self.hand[1].append(blja.deal()[0])
        self.bet.append(self.bet[0])
        self.balance -= self.bet[0]
        printt(f"Your balance is now: {self.balance}")

    def perform_dd(self, blja, i, hand):
        """Creates a players double_down"""
        self.balance -= self.bet[i]
        self.bet[i] *= 2
        printt(f"Double Down Bet: {self.bet[i]}")
        printt(f"Your balance is now: {self.balance}")
        hand.append(blja.deal()[0])
        self.rev_hand(hand)
        if self.has_bust(hand):
            self.bet[i] = 0

    def player_hits(self, hand, blja, i):
        """For asking if a player wants a card"""
        stopped = False
        while not stopped and self.does_hit():
            hand.append(blja.deal()[0])
            self.rev_hand(hand)
            if self.has_bust(hand):
                stopped = True
                self.bet[i] = 0
            if not stopped and self.has_21(hand):
                stopped = True

    def __str__(self):
        return self._name


class Dealer:
    """Dealer Object"""

    def __init__(self):
        """Dealer Initializer"""
        self._name = "Ogier"
        self._hand = []
        self._bj_insur = False
        self._split = False
        self._double_d = False
        self._buy_insur = False

    @property
    def name(self):
        """Name Getter"""
        return self._name

    @property
    def hand(self):
        """Hand Getter"""
        return self._hand

    @property
    def bj_insur(self):
        """Gets value to determine if Dealer has black jack"""
        return self._bj_insur

    @bj_insur.setter
    def bj_insur(self, value):
        """bj_insur setter"""
        self._bj_insur = value

    def show_card(self):
        """Reveals the first card in the dealer's hand"""
        printt(f"{self._name}'s revealed card: {self._hand[0][0]}")

    def rev_hand(self, hand):
        """Reveal the players hand"""
        printt("-" * 50)
        printt(f"{self._name}'s hand:")
        printt(str([card for card in hand])[1:-1])
        printt(f"Hand value: {hand_sum(hand)}")

    def does_split(self):
        """Dealer never splits"""
        return self._split

    def does_double_down(self, curr):
        """Dealer never doubles down"""
        return self._double_d and curr

    def does_hit(self):
        """Dealer's hit algorithm"""
        hit = hand_sum(self._hand[0]) < 17
        if hit:
            printt("I must hit until my hand value is above 16")
        else:
            printt(f"I have {hand_sum(self._hand[0])} so, I'll stand")
        return hit

    def buys_insurance(self):
        """Dealer never buys insurance"""
        return self._buy_insur

    def has_split(self):
        """Checks if a player split hand"""
        return self._split

    def has_bust(self, curr_hand, ind=False):
        """Check if dealer has busted"""
        if hand_sum(curr_hand) > 21:
            if not ind:
                printt(f"{self._name} has Busted")
            return True
        return False

    def black_jack(self, curr_hand):
        """Check if dealer has blackjack"""
        if hand_sum(curr_hand) == 21:
            self._bj_insur = True
            return True
        return False

    def has_21(self, curr_hand):
        """Check if dealer has 21"""
        if hand_sum(curr_hand) == 21:
            printt(f"{self._name} has 21!!!")
            return True
        return False

    def player_hits(self, hand, blja, i):
        """For asking if a player wants a card"""
        stopped = False
        i = 0
        while not stopped and self.does_hit():
            hand.append(blja.deal()[i])
            self.rev_hand(hand)
            if self.has_bust(hand):
                stopped = True
            if not stopped and self.has_21(hand):
                stopped = True
