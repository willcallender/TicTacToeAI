# import tensorflow as tf
# print("Tensorflow successfully loaded")
# import numpy as np
# print("Numpy successfully loaded\n")
import random
from copy import deepcopy

class AI:
    """Template class for all AI"""
    def __init__(self, name):
        self.name = name

    def move(self, board):
        return 0

class RandomAI(AI):
    """AI picks a random legal move"""
    def move(self, board):
        return random.choice(board.legalMoves())

class NextWinAI(AI):
    """Checks to see if any legal moves are winning moves and plays them, if not, then picks randomly"""
    def move(self, game):
        moves = game.legalMoves()
        for pos in moves:
            g = deepcopy(game)
            g.play(pos)
            if g.win() != 0:
                return pos
            
        return random.choice(moves)

class Board:
    """Class for tic-tac-toe style board game."""

    def __init__(self, state=[0, 0, 0, 0, 0, 0, 0, 0, 0]):
        """Initialize board state to a list of zeros."""
        self.state = state

    def win(self):
        """Check for win condition.

        Returns
            1: X wins
            0: Either cat or game still in progress
            -1: O win

        """
        # horizontal wins
        if self.state[0] == self.state[1] and self.state[1] == self.state[2] and self.state[0] != 0:
            return self.state[0]
        if self.state[3] == self.state[4] and self.state[4] == self.state[5] and self.state[3] != 0:
            return self.state[3]
        if self.state[6] == self.state[7] and self.state[7] == self.state[8] and self.state[6] != 0:
            return self.state[6]
        # vertical wins
        for i in range(3):
            if self.state[0+i] == self.state[3+i] and self.state[3+i] == self.state[6+i] and self.state[0+i] != 0:
                return self.state[0+i]
        # horizontal wins
        if (((self.state[0] == self.state[4] and self.state[4] == self.state[8]) or
            (self.state[2] == self.state[4] and self.state[4] == self.state[6])) and self.state[4] != 0):
                return self.state[4]
        return 0

    def tie(self):
        """Check if state is a tie."""
        for i in self.state:
            if i == 0:
                return False
        return True

    def printBoard(self):
        """Pretty print board."""
        printList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(9):
            if self.state[i] == 1:
                printList[i] = 'X'
            elif self.state[i] == -1:
                printList[i] = 'O'
        prt = [str(x) for x in printList]
        print("   |   |   ")
        print('', prt[0], "|", prt[1], "|", prt[2], sep=' ')
        print("   |   |   ")
        print("-----------")
        print("   |   |   ")
        print('', prt[3], "|", prt[4], "|", prt[5], sep=' ')
        print("   |   |   ")
        print("-----------")
        print("   |   |   ")
        print('', prt[6], "|", prt[7], "|", prt[8], sep=' ')
        print("   |   |   ")

    def move(self, p, pos):
        """Check if move is valid.

        p: 1 (player X) or -1 (player O)
        pos: cell (board position)

        If move is valid, set cell to p and return true.
        Otherwise, return false.

        """
        if self.legalMove(pos):
            self.state[pos] = p
            return True
        else:
            return False

    def legalMoves(self):
        """Returns a list of all legal moves"""
        moves = []
        for i in range(9):
            if self.legalMove(i):
                moves.append(i)
        return moves

    def legalMove(self, pos):
        """Returns true if legal move, else false"""
        return self.state[pos] == 0

class Game:
    """Class for playing tic-tac-toe."""

    def __init__(self, board=Board(), turn=1):
        """Initialize board and starting player.

        board is an instance of the Board class.
        turn is either 1 (player X) or -1 (player O).
        """
        self.board = board
        self._turn = turn

    def whoTurn(self):
        """Return current player (either 1 or -1)."""
        return self._turn

    def whoTurnStr(self):
        """Returns user friendly player"""
        if self._turn == 1:
            return 'X'
        else:
            return 'O'

    def newTurn(self):
        """Switch current player."""
        self._turn = self._turn * -1

    def play(self, pos):
        """Make move by current player in position given by pos.

        Return true if move made successfully, false if not.
        """
        if self.board.move(self._turn, pos):
            self.newTurn()
            return True
        else:
            return False

    def win(self):
        """Return if game is won and by which player."""
        return self.board.win()

    def winStr(self):
        """Translate win method into text.

        Return 'X' (for 1), 'O' (for -1), and 'No winner' otherwise.
        """
        if self.board.win() == 1:
            return 'X'
        elif self.board.win() == -1:
            return 'O'
        else:
            return 'No winner'

    def tie(self):
        """Return True or False if game is a tie."""
        return self.board.tie()

    def printBoard(self):
        """Pretty print tic-tac-toe board."""
        self.board.printBoard()

    def legalMoves(self):
        """Returns list of legal moves on internal board object"""
        return self.board.legalMoves()


game = Game()
##while game.win() == 0 and not game.tie():
##    print("{}'s turn, input move".format(game.whoTurnStr()))
##    game.printBoard()
##    try:
##        pos = int(input())-1
##        if not game.play(pos):
##            print("Illegal move!")
##    except:
##        print("Move not recognized")
##
##if not game.tie():
##    print("{} wins!".format(game.winStr()))
##else:
##    print("Tie")
##game.printBoard()

ai = NextWinAI("Howard")
while game.win() == 0 and not game.tie():
    game.printBoard()
    if game.whoTurn() == 1:
        print("Player turn, input move")
        try:
            pos = int(input())-1
            if not game.play(pos):
                print("Illegal move!")
        except:
            print("Move not recognized")
    else:
        print("Computer turn")
        game.play(ai.move(game))

print(game.win(), game.tie())
game.printBoard()
if not game.tie():
    print("{} wins!".format(game.winStr()))
else:
    print("Tie")