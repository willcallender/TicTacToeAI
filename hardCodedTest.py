# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 09:50:01 2019

@author: William Callender
"""

def hardCodedTest(n):
    randomWins = 0
    nextWinWins = 0
    winPreventWins = 0
    game = Game()
    for i in range(n):
        game.reset()
        (winner, tie) = game.play(RandomAI(), NextWinAI())
        if winner == 1:
            randomWins += 1
        elif winner == -1:
            nextWinWins += 1
    
        game.reset()
        (winner, tie) = game.play(NextWinAI(), RandomAI())
        if winner == 1:
            nextWinWins += 1
        elif winner == -1:
            randomWins += 1
    
        game.reset()
        (winner, tie) = game.play(NextWinAI(), WinPreventAI())
        if winner == 1:
            nextWinWins += 1
        elif winner == -1:
            winPreventWins += 1
    
        game.reset()
        (winner, tie) = game.play(WinPreventAI(), NextWinAI())
        if winner == 1:
            winPreventWins += 1
        elif winner == -1:
            nextWinWins += 1
    
        game.reset()
        (winner, tie) = game.play(RandomAI(), WinPreventAI())
        if winner == 1:
            randomWins += 1
        elif winner == -1:
            winPreventWins += 1
    
        game.reset()
        (winner, tie) = game.play(WinPreventAI(), RandomAI())
        if winner == 1:
            winPreventWins += 1
        elif winner == -1:
            randomWins += 1
    
    print(randomWins, nextWinWins, winPreventWins)
