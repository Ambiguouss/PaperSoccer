from Players.Player import Player
from Enviroment import *
import numpy as np

class RandomPlayer(Player):
    def make_moves(self,board):
        ball = board.ball
        move = []
        while ball in board.touched_fields:
            valid_moves=[]
            for e in board.board.edges(ball):
                if board.board.edges[e]['weight']==0:
                    valid_moves.append(e)
            if len(valid_moves)==0:
                break
            move_to_add=valid_moves[np.random.choice(len(valid_moves))]
            board.board.edges[move_to_add]['weight']=1
            move_coord=tuple(b - a for a, b in zip(ball, move_to_add[1]))
            move.append(move_coord)
            ball = move_to_add[1]
        return move


                