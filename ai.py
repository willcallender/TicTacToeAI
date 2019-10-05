from game import Game
import random
from copy import deepcopy


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
