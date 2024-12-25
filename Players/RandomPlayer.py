from Players.Player import Player
from Enviroment import *
import numpy as np

class RandomPlayer(Player):

    def __init__(self,board):
        self.board=board
    
    def update_board(self,board):
        self.board=board

    def make_moves(self,board,last_move):
        self.update_board(board)
        ball = self.board.ball
        move = []
        while ball in self.board.touched_fields:
            valid_moves=[]
            for e in self.board.board_graph.edges(ball):
                if self.board.board_graph.edges[e]['weight']==0:
                    valid_moves.append(e)
            if len(valid_moves)==0:
                break
            move_to_add=valid_moves[np.random.choice(len(valid_moves))]
            self.board.board_graph.edges[move_to_add]['weight']=1
            move_coord=tuple(b - a for a, b in zip(ball, move_to_add[1]))
            move.append(move_coord)
            ball = move_to_add[1]
        return move


                
