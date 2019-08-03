import ai
from game import Game


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
            print("game {}--{}: {}, {}: {}, tie: {}".format(i + 1,
                                                            player1.name,
                                                            player1.wins,
                                                            player2.name,
                                                            player2.wins,
                                                            ties))
    return (player1.wins, player2.wins, ties)


player1 = ai.WinPreventAI(name="WinPrevent")
player2 = ai.MonteCarloAI(name="MonteCarlo", depth=100)
results = simulation(player1, player2, num_games=1000, verbose=True)
print("{}: {}, {}: {}, tie: {}".format(player1.name, results[0],
                                       player2.name, results[1],
                                       results[2]))
