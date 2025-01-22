from Players.Player import Player
from Enviroment import *
from Enviroment.GameRules import GameRules
from Players.utils import find_lethal
import numpy as np

class betterRandomPlayer(Player):

    def __init__(self,board):
        self.board=board
    
    def update_board(self,board):
        self.board=board

    def make_moves(self,board,last_move):
        self.update_board(board)
        move = []
        lethal = find_lethal(board,self.player)
        if lethal is not None:
            return lethal
        valid_moves = GameRules.find_valid_moves(board)
        if len(valid_moves)==0:
            return []
        random_index = np.random.choice(len(valid_moves))
        move = valid_moves[random_index]
        return move


                
