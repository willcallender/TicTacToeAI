import tensorflow as tf
print("Tensorflow successfully loaded")
import random
from copy import deepcopy
import numpy as np


class Player:
    """Template class for all Players (human and computer)."""

    def __init__(self, name="Howard"):
        """Assign name for player."""
        self.name = name

    def move(self, game):
        """Make player move. Implemented in child classes."""
        pass


class Human(Player):
    """Class for human player."""

    def move(self, game):
        """Prompt user for moves and return them to game."""
        game.printBoard()
        print("Input move")
        return int(input()) - 1

class RandomAI(Player):
    """AI picks a random legal move."""

    def move(self, game):
        """Make random choice from legal moves."""
        return random.choice(game.legalMoves())


class NextWinAI(Player):
    """Play winning move, otherwise play random move."""

    def move(self, game):
        """Check if a winning move exists.

        Return winning move, if available; otherwise, return random move.
        """
        moves = game.legalMoves()
        for pos in moves:
            g = deepcopy(game)
            g.move(pos)
            if g.win() != 0:
                return pos

        return random.choice(moves)


class WinPreventAI(Player):
    """Like NextWinAI, but also check opponent's next move to avoid loss."""

    def move(self, game):
        """Play to win first, avoid loss second.

        1) Play winning move.
        2) Block opponent's winning move.
        3) If none of the above, play random move.
        """
        moves = game.legalMoves()
        for pos in moves:
            g = deepcopy(game)
            g.move(pos)
            if g.win() != 0:
                return pos
        for pos in moves:
            g = deepcopy(game)
            g._turn = g.whoTurn() * -1
            g.move(pos)
            if g.win() != 0:
                return pos

        return random.choice(moves)

class MonteCarloPredictor(Player):
    """Doesn't return move, returns probability of win from a given position, player to move must always be X"""
    def winProb(self, state, n=1000):      # returns probability of win, state must always have player to analyze as X
        wins = 0
        losses = 0  # losses and ties may be utilized in the future
        ties = 0
        for _ in range(n):
            s = deepcopy(state)
            g = Game(turn=-1)
            g.board.state = s
            winner, tie = g.play(RandomAI(), RandomAI())
            if not tie:
                if winner == 1:   # if not a tie and winner was X
                    wins = wins + 1
                else:
                    losses = losses + 1
            else:
                ties = ties + 1
        return wins/n

class Board:
    """Class for tic-tac-toe style board game."""

    def __init__(self):
        """Initialize board state to a list of zeros."""
        self.state = [0] * 9

    def win(self):
        """Check for win condition.

        Returns
            1: X wins
            0: Either cat or game still in progress
            -1: O win

        """
        winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                                [0, 4, 8], [2, 4, 6]]

        # check if any winning combinations are all 1s or -1s
        for i, j, k in winning_combinations:
            if self.state[i] == self.state[j] == self.state[k] != 0:
                return self.state[i]  # return winning player
        # otherwise return 0
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
        """Return a list of all legal moves."""
        moves = []
        for i in range(9):
            if self.legalMove(i):
                moves.append(i)
        return moves

    def legalMove(self, pos):
        """Return true if legal move, else false."""
        return self.state[pos] == 0


class Game:
    """Class for playing tic-tac-toe."""

    def __init__(self, turn=1, show_moves=False):
        """Initialize board and starting player.

        board is an instance of the Board class.
        turn is either 1 (player X) or -1 (player O).
        """
        self.board = Board()
        self._turn = turn
        self.show_moves = show_moves

    def whoTurn(self):
        """Return current player (either 1 or -1)."""
        return self._turn

    def whoTurnStr(self):
        """Return user friendly player."""
        if self._turn == 1:
            return 'X'
        else:
            return 'O'

    def newTurn(self):
        """Switch current player."""
        self._turn *= -1

    def play(self, player1, player2):
        """Play tic-tac-toe."""
        players = {1: player1, -1: player2}
        while not self.over():
            current_player = players[self._turn]
            move = current_player.move(self)
            try:
                if not self.move(move):
                    print("Illegal move!")
            except:
                print("Move not recognized")
            if self.show_moves:
                self.printBoard()
        return self.win(), self.tie()

    def reset(self):
        """Reset the board and turn."""
        self.board = Board()
        self._turn = 1

    def move(self, pos):
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
    
    def over(self):
        """Returns true if game is over, otherwise false"""
        if self.win() != 0 or self.tie():
            return True
        return False

    def printBoard(self):
        """Pretty print tic-tac-toe board."""
        self.board.printBoard()
        predict = MonteCarloPredictor()
        print(predict.predScore(self.board.state))
        print("\n\n")

    def legalMoves(self):
        """Return list of legal moves on internal board object."""
        return self.board.legalMoves()

n=1000000
games = []
game = Game()
pred = MonteCarloPredictor()
ai = RandomAI()
for i in range(n):
    g = deepcopy(game)
    while not g.over():
        g.move(ai.move(g))
        games.append((deepcopy(g.board.state), pred.winProb(deepcopy(g.board.state))))

trainLen = int(len(games)*0.8)
trainGames = [games[i] for i in range(trainLen)]
testGames = [games[i] for i in range(trainLen, len(games))]
xtrain = [i[0] for i in trainGames]
ytrain = [i[1] for i in trainGames]
xtest = [i[0] for i in testGames]
ytest = [i[1] for i in testGames]
npxtrain = np.array(xtrain)
npytrain = np.array(ytrain)
npxtest = np.array(xtest)
npytest = np.array(ytest)
np.savetxt('xtrain.txt', npxtrain)
np.savetxt('ytrain.txt', npytrain)
np.savetxt('xtest.txt', npxtest)
np.savetxt('ytest.txt', npytest)

#inputs = tf.keras.Input(shape=(9,))
#x = tf.keras.layers.Dense(128, activation='elu')(inputs)
#x = tf.keras.layers.Dense(128, activation='elu')(x)
#x = tf.keras.layers.Dense(128, activation='relu')(x)
#outputs = tf.keras.layers.Dense(1, activation='softmax')(x)
#model = tf.keras.Model(inputs = inputs, outputs=outputs)
#
#model.summary()
#
#model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
#model.fit(npxtrain, npytrain, epochs=3)
#model.evaluate(xtest, ytest)