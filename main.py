from Players.RandomPlayer import RandomPlayer
from Players.MonteCarloPlayer import MonteCarloPlayer
from Enviroment.Game import Game
from Enviroment.Board import Board
from Enviroment.GameRules import GameRules
#from Players.MonteCarlo import MonteCarlo
import numpy as np




#board.make_moves([(1,1)],1)
#board.make_moves([(-1,0)],2)
#print(GameRules.find_valid_moves(board))
#board.draw()
#board.make_moves([(1,1)],1)
#board.make_moves([(-1,0)],2)
#board.draw()
#v = GameRules.find_valid_moves(board)
#for x in v:
#    print(x)
#

for i in range(100):
    np.random.seed(i)
    board=Board()
    player1 = MonteCarloPlayer(board,10)
    player2=RandomPlayer(board)
    game = Game(board,player1,player2)
    game.start_game(res=True)

game.board.draw()
