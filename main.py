from Players.RandomPlayer import RandomPlayer
from Players.BadPlayers.MonteCarloPlayer import MonteCarloPlayer
from Players.MonteCarloPlayer2 import MonteCarloPlayer2
from Players.betterRandom import betterRandomPlayer
from Players.DeepQPlayer import DeepQPlayer
from Players.HumanPlayer import HumanPlayer
from Enviroment.Game import Game
from Enviroment.Board import Board
from Enviroment.GameRules import GameRules
from Players.utils import test
#from Players.MonteCarlo import MonteCarlo
import numpy as np
from copy import deepcopy

np.random.seed(4)
board = Board()
dqp = DeepQPlayer(board)
#dqp.fit(10)
dqp.main_network.load_weights("savedModels/DeepQ/deepQv1.2BIGGammaLR0.001LesserUpdates.weights.h5")
#g = Game(board,dqp,MonteCarloPlayer2(board,20))
#res = g.start_game(draw=True)
#g.board.draw()

g = Game(board,dqp,betterRandomPlayer(board))
res = g.start_game(draw=True)
g.board.draw()

