from Enviroment.GameRules import GameRules
from copy import deepcopy
from Enviroment.Board import Board
from Enviroment.Game import Game
import numpy as np

def find_lethal(board,player):
    'player=0 or 1'
    copy_board=board
    for valid_move in GameRules.find_valid_moves(copy_board):
        new_board=deepcopy(copy_board) #ughhhhh
        new_board.make_moves(valid_move)
        if GameRules.in_player1_goal(new_board) and player==1:
            return valid_move
        if GameRules.in_player2_goal(new_board) and player==0:
            return valid_move
    return None


def test(player1,player2):
    p1=0
    p2=0
    for i in range(100):
        board=Board()
        g = Game(board,player1,player2)
        res = g.start_game()
        print(f"player {res+1} win")
        if res==0:
            p1+=1
        else:
            p2+=1
            g.board.draw()
    return p1/(p1+p2)
