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
"""Executable File for Black Jack"""

from blackjackgame import game

if __name__ == '__main__':
    MY_GAME = game.BlackJackGame()
    MY_GAME.run()
