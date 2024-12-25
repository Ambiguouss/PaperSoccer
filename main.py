from Players.RandomPlayer import RandomPlayer
from Enviroment.Game import Game
from Enviroment.Board import Board
import numpy as np



l = [(0,0),(1,1)]
k=np.asarray(l)
print(k)

game = Game(Board(),RandomPlayer(),RandomPlayer())
game.start_game()