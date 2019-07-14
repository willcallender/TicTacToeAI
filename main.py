# import tensorflow as tf
# print("Tensorflow successfully loaded")
# import numpy as np
# print("Numpy successfully loaded\n")


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

        p: 1 (player X) or 0 (player O)
        pos: cell (board position)

        If move is valid, set cell to p.
        Otherwise, return exception.

        """
        if self.state[pos] == 0:
            self.state[pos] = p
        else:
            raise Exception('Invalid move, space already occupied')


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
        """Return current player (either X or O)."""
        if self._turn == 1:
            return 'X'
        return 'O'

    def newTurn(self):
        """Switch current player."""
        if self._turn == 1:
            self._turn = -1
        else:
            self._turn = 1

    def play(self, pos):
        """Make move by current player in position given by pos.

        Return exception raised by board if move is invalid.
        """
        self.board.move(self._turn, pos)
        self.newTurn()

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


game = Game()
while game.win() == 0 and not game.tie():
    print("{}'s turn, input move".format(game.whoTurn()))
    game.printBoard()
    try:
        pos = int(input()) - 1
        game.play(pos)
    except:
        print("Invalid move!")
if not game.tie():
    print("{} wins!".format(game.win()))
else:
    print("Tie")
