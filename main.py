from Players.RandomPlayer import RandomPlayer
from Players.MonteCarloPlayer import MonteCarloPlayer
from Players.MonteCarloPlayer2 import MonteCarloPlayer2
from Players.betterRandom import betterRandomPlayer
from Players.DeepQPlayer import DeepQPlayer
from Enviroment.Game import Game
from Enviroment.Board import Board
from Enviroment.GameRules import GameRules
#from Players.MonteCarlo import MonteCarlo
import numpy as np
from copy import deepcopy


np.random.seed(1)
board = Board()
dqp = DeepQPlayer(board)
dqp.fit(30)
dqp.main_network.save_weights('savedModels/DeepQ/deepQv0.1.weights.h5')
print("fitted")
g = Game(board,DeepQPlayer(board),betterRandomPlayer(board))
res = g.start_game(res=True)
g.board.draw()
print(f'player{res+1} win')
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
#mc=0
#random=0
#with open('Results/MonteCarloVSRandom2.txt', 'w') as file:
#    # Print to the file
#
#    for i in range(100):
#        np.random.seed(i)
#        board=Board()
#        player1 = MonteCarloPlayer2(deepcopy(board),32)
#        player2=betterRandomPlayer(deepcopy(board))
#        game = Game(board,player1,player2)
#        res = game.start_game(res=True)
#        print(f'player{res+1} win')
#        if res==0:
#            mc+=1
#        else:
#            random+=1
#
#    print(f'monte carlo blue site win ratio:{mc/(mc+random)}',file=file)
#
#    mc=0
#    random=0
#    for i in range(100):
#        np.random.seed(i)
#        board=Board()
#        player2 = MonteCarloPlayer2(deepcopy(board),32)
#        player1=betterRandomPlayer(deepcopy(board))
#        game = Game(board,player1,player2)
#        res = game.start_game(res=True)
#        print(f'player{res+1} win')
#        if res==1:
#            mc+=1
#        else:
#            random+=1
#
#    print(f'monte carlo red site win ratio:{mc/(mc+random)}',file=file)

