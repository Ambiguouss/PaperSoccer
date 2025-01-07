from Players.Player import Player
from Enviroment import *
from Enviroment.GameRules import GameRules
import numpy as np

class betterRandomPlayer(Player):

    def __init__(self,board):
        self.board=board
    
    def update_board(self,board):
        self.board=board

    def make_moves(self,board,last_move):
        self.update_board(board)
        move = []
        valid_moves = GameRules.find_valid_moves(board)
        if len(valid_moves)==0:
            return []
        random_index = np.random.choice(len(valid_moves))
        move = valid_moves[random_index]
        return move


                
