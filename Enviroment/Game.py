import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy
from Enviroment.Board import Board,GameState
from Enviroment.GameRules import GameRules

class Game:
    def __init__(self,board,player1,player2):
        self.board=board
        self.player1=player1
        self.player2=player2
    def start_game(self,draw=False):
        player=self.player1
        opponent = self.player2
        last_move=None
        while True:
            moves = player.make_moves(copy.deepcopy(self.board),last_move)
            game_state = self.board.make_moves(moves,1 if player==self.player1 else 2)
            last_move=moves
            if game_state == False:
                player.handle_loss()
                opponent.handle_win()
                self.result=f"player{1 if opponent==self.player1 else 2} win"
                break
            elif GameRules.in_player1_goal(self.board):
                self.player1.handle_loss()
                self.player2.handle_win()
                self.result="player2 win"
                break
            elif GameRules.in_player2_goal(self.board):
                self.player2.handle_loss()
                self.player1.handle_win()
                self.result="player1 win"
                break
            if draw:
                self.board.draw()
            player,opponent = opponent,player