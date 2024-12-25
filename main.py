from Players.RandomPlayer import RandomPlayer
from Players.MonteCarloTrainer import MonteCarloTrainer,load_tree,save_tree
from Enviroment.Game import Game
from Enviroment.Board import Board
from Enviroment.GameRules import GameRules
from Players.MonteCarlo import MonteCarlo
import numpy as np




board=Board()
#print(GameRules.find_valid_moves(board))
#board.make_moves([(1,1)],1)
#board.make_moves([(-1,0)],2)
#board.draw()
#v = GameRules.find_valid_moves(board)
#for x in v:
#    print(x)
#
board= Board()
mct = MonteCarloTrainer(board)
x= mct.train()
save_tree(x,"savedModels/MonteCarlo/1000.json")
#print(x.number_of_wins,x.number_of_visits)


t = load_tree("savedModels/MonteCarlo/1000.json")
print(t.number_of_wins,t.number_of_visits)
for child in t.children:
    print(child.number_of_visits)
board = Board()
player1 = MonteCarlo(board,t,1)
#player1=RandomPlayer(board)
player2=RandomPlayer(board)
game = Game(board,player1,player2)
game.start_game(draw=True)
game.board.draw()