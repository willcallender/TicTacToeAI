# import tensorflow as tf
# print("Tensorflow successfully loaded")
import random
from copy import deepcopy
# import numpy as np


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
            if g.evaluate() in [1, -1]:
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
            if g.evaluate() in [1, -1]:
                return pos
        for pos in moves:
            g = deepcopy(game)
            g._turn = g.whoTurn() * -1
            g.move(pos)
            if g.evaluate() in [1, -1]:
                return pos

        return random.choice(moves)


class MonteCarloAI:
    """Implement simple Monte Carlo Search."""

    def __init__(self, name="Monte Carlo", depth=25, turn=1):
        """Assign name, random playout depth, and current turn."""
        self.name = name
        self.depth = depth
        self.turn = turn

    def move(self, game):
        """Evaluate self.depth playouts for each legal move.

        Return move with the best average score of random playouts.
        """
        moves = game.legalMoves()
        evaluations = {}
        for move in moves:
            evaluations[move] = 0
            for _ in range(self.depth):
                g = Game()
                g.board.state = [-self.turn * cell
                                 for cell in game.board.state]
                g.board.state[move] = -1
                evaluation = (g.play(RandomAI(), RandomAI()) * -1 + 1) / 2
                evaluations[move] += evaluation
        return max(evaluations, key=evaluations.get)


class Board:
    """Class for tic-tac-toe style board game."""

    def __init__(self):
        """Initialize board state to a list of zeros."""
        self.state = [0] * 9

    def evaluate(self):
        """Evaluate board.

        Returns 'X', 'O', 'CAT', or None.

        """
        win = self.win()
        if win:
            return win
        tie = self.tie()
        if tie:
            return 0
        else:
            return None

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
        while self.evaluate() is None:
            current_player = players[self._turn]
            move = current_player.move(self)
            try:
                if not self.move(move):
                    print("Illegal move!")
            except:
                print("Move not recognized")
            if self.show_moves:
                self.printBoard()
        return self.evaluate()

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

    def evaluate(self):
        """Return board evaluation."""
        return self.board.evaluate()

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
        print("\n\n")

    def legalMoves(self):
        """Return list of legal moves on internal board object."""
        return self.board.legalMoves()


def simulation(player1, player2, num_games=100, verbose=False):
    """Docstring."""
    player1.wins = 0
    player2.wins = 0
    ties = 0
    game = Game()
    for i in range(num_games):
        game.reset()
        if i % 2 == 0:
            X, O = player1, player2
            X.turn, O.turn = 1, -1
        else:
            X, O = player2, player1
            X.turn, O.turn = -1, 1
        evaluation = game.play(X, O)
        if evaluation == 1:
            X.wins += 1
        elif evaluation == -1:
            O.wins += 1
        else:
            ties += 1
        if verbose:
            # print("{} game(s) played ...".format(i + 1))
            print("game {}--{}: {}, {}: {}, tie: {}".format(i + 1,
                                                            player1.name,
                                                            player1.wins,
                                                            player2.name,
                                                            player2.wins,
                                                            ties))
    return (player1.wins, player2.wins, ties)


player1 = WinPreventAI(name="WinPrevent")
player2 = MonteCarloAI(name="MonteCarlo", depth=100)
results = simulation(player1, player2, num_games=1000, verbose=True)
print("{}: {}, {}: {}, tie: {}".format(player1.name, results[0],
                                       player2.name, results[1],
                                       results[2]))
