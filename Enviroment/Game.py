import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy
from Enviroment.Board import Board,GameState


class Game:
    def __init__(self,board,player1,player2):
        self.board=board
        self.player1=player1
        self.player2=player2
    def start_game(self):
        player=self.player1
        while True:
            print(player==self.player1)
            try:
                moves = player.make_moves(copy.deepcopy(self.board))
                game_state = self.board.make_moves(moves,1 if player==self.player1 else 2)
            except Exception as e:
                print(player==self.player1)
                if player == self.player2:
                    self.player1.handle_win()
                    self.player2.handle_loss()
                    self.result = "player1 win"
                else:
                    self.player2.handle_win()
                    self.player1.handle_loss()
                    self.result = "player2 win"
                print(e)
                break
            if game_state == GameState.WinFirst:
                self.player1.handle_win()
                self.player2.handle_loss()
                self.result="player1 win"
                break
            elif game_state == GameState.WinSecond:
                self.player1.handle_loss()
                self.player2.handle_win()
                self.result="player2 win"
                break
            player = self.player1 if player==self.player2 else self.player2
        print(self.result)
        self.board.draw()