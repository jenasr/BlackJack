#! /usr/bin/env python3
# Joseph Nasr
# CPSC 386-01
# 2022-04-04
# jenasr@csu.fullerton.edu
# @jenasr
#
# Lab 03-00
#
# File for Miscelaneuos functions
#
"""To Make things simpler"""

from time import sleep

TIME_TO_WAIT = 1
RULES = 4


def printt(output, amount=TIME_TO_WAIT, where_to=1):
    """For printing with a waiting time before or after"""
    if where_to:
        print(output)
        sleep(amount)
    else:
        sleep(amount)
        print(output)


def display_rules():
    """Displays the rules"""
    printt("The rules are as follows:", RULES)
    printt(
        "Each player will bet a certain amount of money each round from their"
        " bankroll",
        RULES,
    )
    printt("Then each player will be dealt a hand of 2 cards face-up", RULES)
    printt(
        "I, however, will have 1 card face-up and 1 card" " face-down", RULES
    )
    printt(
        "Each card has a rank and suit. Suits do not matter in this" " game",
        RULES,
    )
    printt(
        "Rank of the card (the numbers or letters) determine the value of"
        " the card",
        RULES,
    )
    printt(
        "Numbers are exactly their value; Jack, Queen, King are valued"
        " at 10",
        RULES,
    )
    printt("Ace can be valued at 1 or 11, it is the player’s choice", RULES)
    printt(
        "After all the cards are dealt you may be asked to buy insurance", RULES
    )
    printt("Insurance is bought when you believe I have a blackjack", RULES)
    printt(
        "Simply, when I have a 10 or Ace showing, you want to buy insurance",
        RULES,
    )
    printt(
        "If I have blackjack, then you will be paid the amount you bet", RULES
    )
    printt("If I don’t, you lose your insurance bet", RULES)
    printt(
        "NOTE: insurance bet differs from the bet you placed at the start"
        " of the round",
        RULES,
    )
    printt("It is therefore known as a side bet", RULES)
    printt("Now to turn play:", RULES)
    printt("Your goal for the turn is to get as close to 21 as possible", RULES)
    printt(
        "If you get 21 based on the first 2 cards you were dealt you have"
        " a blackjack",
        RULES,
    )
    printt("You will not be asked to do anything further", RULES)
    printt(
        "If you don’t have 21, you are going to try to get as close to 21 as"
        " possible",
        RULES,
    )
    printt(
        "However, if you go over 21 you have busted, and lose your money", RULES
    )
    printt("Your turn can consist of a few decisions", RULES)
    printt("The first would be to split your hand", RULES)
    printt(
        "Splitting means, you take your hand with 2 cards of identical rank",
        RULES,
    )
    printt("And treat them as 2 separate hands", RULES)
    printt(
        "When this happens, you must place a bet equal to your original"
        " on the 2nd hand",
        RULES,
    )
    printt(
        "I will then deal a card to each hand, so they are valid hand size",
        RULES,
    )
    printt("You will then play each hand separately", RULES)
    printt("The second decision would be to double down", RULES)
    printt(
        "This means, you double your bet for that hand, but you only want"
        " one more card",
        RULES,
    )
    printt("The third is to hit", RULES)
    printt(
        "Hitting means you want another card to be added to your hand", RULES
    )
    printt(
        "The card dealt to that hand will add its rank onto the value"
        " of that hand",
        RULES,
    )
    printt("I am required to hit until I have a hand value >=17", RULES)
    printt("If I go over 21 then I bust", RULES)
    printt("In other words, try to get as close to 21 as possible", RULES)
    printt("But if you are worried about busting, try to beat me", RULES)
    printt("At the end of all players' turns, payout will begin", RULES)
    printt("If you have busted, you lose that hand", RULES)
    printt("If your hand value < mine you have lost that hand", RULES)
    printt("Losing means you lose the money you bet for that hand", RULES)
    printt("If your hand value > mine you have won that hand", RULES)
    printt(
        "Winning means you earn money equal to what you bet for that hand",
        RULES,
    )
    printt("If your hand value = mine you have pushed that hand", RULES)
    printt("Pushing means you simply keep the money you bet", RULES)
    printt("-" * 65)
    printt("-" * 65)
