#! /usr/bin/env python3
# Joseph Nasr
# CPSC 386-01
# 2022-04-04
# jenasr@csu.fullerton.edu
# @jenasr
#
# Lab 03-00
#
# Black Jack Simulation
#
"""For the Game"""
from os.path import exists
from pickle import dump, load, HIGHEST_PROTOCOL
from .functions import printt, display_rules
from .player import Player, Dealer, hand_sum
from .cards import Deck, card_value, reshuffle

PICKFILE = "players.pckl"


def to_file(players):
    """Write the list players to the file pickle_file."""
    with open(PICKFILE, "wb") as file_handle:
        dump(players, file_handle, HIGHEST_PROTOCOL)
        # want to know what the highest protocol means


def from_file():
    """Read pickle_file, decode it, and return it as players."""
    with open(PICKFILE, "rb") as file_handle:
        players = load(file_handle)
        # work with a file in this scope
    return players


def insurance(plr):
    """Insurance Handler"""
    printt(f"{plr.name}, your balance is: {plr.balance}")
    curr_bet = float(input(f"How much? "))
    while curr_bet > plr.balance or curr_bet < 1:
        printt(f"{plr.name} your bet is invalid")
        printt(f"Your balance is: {plr.balance}")
        curr_bet = float(input("Provide a valid bet: "))
    plr.side_bet = curr_bet
    plr.balance -= curr_bet
    printt(f"Your balance is now: {plr.balance}")


class BlackJackGame:
    """Object for Black Jack Game"""

    def __init__(self):
        """Game initializer"""
        self._players = []
        self._dealer = Dealer()

    def deal_cards(self, blja):
        """Deal each player 2 cards"""
        for j in range(2):
            printt("Dealing")
            for plr in self._players:
                if j == 0:
                    temp_hand = []
                    temp_hand.append(blja.deal()[0])
                    plr.hand.append(temp_hand)
                else:
                    plr.hand[0].append(blja.deal()[0])
        for plr in self._players[:-1]:
            printt(f"{plr.name}: {plr.hand[0][0]}, {plr.hand[0][1]}")
        self._dealer.show_card()
        for plr in self._players:
            if (
                card_value(self._dealer.hand[0][0]) == 10
                or self._dealer.hand[0][0].rank == "Ace"
            ):
                if plr.buys_insurance():
                    insurance(plr)

    def get_bets(self):
        """Gets each players bets"""
        printt("-" * 50)
        printt("-" * 50)
        printt("-" * 50)
        printt("Players please place your bets: ")
        for i, plr in enumerate(self._players[:-1]):
            printt(f"{plr.name}, your balance is: {plr.balance}")
            curr_bet = float(input(f"({i+1}) {plr.name}: "))
            while curr_bet > plr.balance or curr_bet < 1:
                printt(f"{plr.name} your bet is invalid")
                printt(f"Your balance is: {plr.balance}")
                curr_bet = float(input("Provide a valid bet: "))
            plr.balance -= curr_bet
            printt(f"Your balance is now: {plr.balance}")
            plr.bet.append(curr_bet)

    def players_turn(self, plr, blja):
        """Player Turn Handler"""
        plr.rev_hand(plr.hand[0])
        if not isinstance(plr, Dealer):
            self._dealer.show_card()
        # If dealer shows 10 or 11 ask for insurance
        # If a player has 21 at start they have blackjack
        if (
            not plr.black_jack(plr.hand[0])
            and plr.hand[0][0].rank == plr.hand[0][1].rank
            and plr.does_split()
        ):
            plr.perform_split(blja)
        elif plr.black_jack(plr.hand[0]):
            printt(f"{plr.name}, you have a Black Jack!!!")
        for i, hand in enumerate(plr.hand):
            if plr.has_split():
                printt("-" * 50)
                printt(f"Hands: ")
                printt(f"1) {str(plr.hand[0])[1:-1]}")
                printt(f"2) {str(plr.hand[1])[1:-1]}")
                printt("-" * 50)
                printt(f"Hand {i+1}: ")
                plr.rev_hand(hand)
            if not plr.black_jack(plr.hand[i]):
                if plr.does_double_down(i):
                    plr.perform_dd(blja, i, hand)
                else:
                    plr.player_hits(hand, blja, i)
        return plr

    def payout(self):
        """Pay or take money from players"""
        printt("-" * 50)
        printt("Payout")
        printt("-" * 50)
        self._dealer.rev_hand(self._dealer.hand[0])
        for plr in self._players[:-1]:
            if not self._dealer.bj_insur and plr.side_bet > 0:
                printt("-" * 50)
                printt(f"{plr.name}, you have lost insurance")
                plr.side_bet = 0
            elif self._dealer.bj_insur and plr.side_bet > 0:
                printt("-" * 50)
                printt(f"{plr.name}, you have won insurance")
            plr.side_bet *= 2
            for i, hand in enumerate(plr.hand):
                plr.rev_hand(hand)
                h_val = hand_sum(hand)
                dealh_val = hand_sum(self._dealer.hand[0])
                if not plr.has_bust(hand) and not self._dealer.has_bust(
                    self._dealer.hand[0]
                ):
                    if h_val < dealh_val:
                        printt(f"{plr.name}, you have lost this hand")
                        printt("-" * 50)
                        plr.bet[i] = 0
                    elif h_val > dealh_val:
                        printt(f"{plr.name}, you have won this hand")
                        printt("-" * 50)
                    else:
                        printt(f"{plr.name}, you have pushed this hand")
                        printt("-" * 50)
                        plr.bet[i] *= 0.5
                elif self._dealer.has_bust(
                    self._dealer.hand[0], True
                ) and not plr.has_bust(hand, True):
                    printt(f"{plr.name}, you have won this hand")
                    printt("-" * 50)
                elif plr.has_bust(hand, True):
                    printt(f"{plr.name}, you have lost this hand")
                    printt("-" * 50)
                    plr.bet[i] = 0
            for bets in plr.bet:
                plr.balance += 2 * bets
            plr.balance += plr.side_bet
            printt(f"{plr.name}, your balance is {plr.balance}")

    def reset(self):
        """Resets the players and dealer"""
        for plr in self._players[:-1]:
            plr.hand.clear()
            plr.bet.clear()
            plr.side_bet = 0
            if plr.balance == 0:
                printt(f"{plr.name} you balance is 0; Reset to 10000.0")
                plr.balance = 10000.0
        self._dealer.hand.pop()
        self._dealer.bj_insur = False

    def run(self):
        """Main Game Loop"""
        printt("Hello welcome to Virtual Black Jack", 1)
        printt(f"I will be your dealer {self._dealer.name}")
        display_rules()
        num_players = input("How many players are there? 1-4: ")
        saved_players = []
        if exists(PICKFILE):
            saved_players = from_file()
            # print(saved_players)
        for player in range(int(num_players)):
            p_number = player + 1
            temp_name = input(f"Player {p_number} enter your name: ")
            added = False
            for index, saved in enumerate(list(saved_players)):
                if saved.name == temp_name:
                    self._players.append(saved_players.pop(index))
                    added = True
            if not added:
                self._players.append(Player(temp_name))
        self._players.append(self._dealer)
        printt("May the games begin!")
        printt("Creating Deck")
        blja = reshuffle()
        done = False
        while not done:
            # Get each players bet
            self.get_bets()
            self.deal_cards(blja)
            printt("-" * 50)
            printt("Turns")
            printt("-" * 50)
            for plr in self._players:
                plr = self.players_turn(plr, blja)
            self.payout()
            self.reset()
            printt("-" * 50)
            if blja.reached:
                blja = reshuffle()
            resp = input(f"{self._players[0].name} want to play again? ")
            done = resp not in ("y", "Y")
            # for i, plr in enumerate(self._players):
        printt("Saving Players")
        printt("...")
        printt("...")
        printt("...")
        printt("Thanks for playing!")
        self._players.pop()
        to_file(self._players + saved_players)
