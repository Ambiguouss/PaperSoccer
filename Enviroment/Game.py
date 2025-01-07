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
    
    def start_game(self,draw=False,res=False,goes_first=0):
        player, opponent = self._initialize_players(goes_first)

        if GameRules.in_player1_goal(self.board):
            return self._handle_game_end(self.player2, self.player1, "player2 win")
        elif GameRules.in_player2_goal(self.board):
            return self._handle_game_end(self.player1, self.player2, "player1 win")
        #problem if game is over already but not by goal
        moves=None
        while True:
            moves = player.make_moves(copy.deepcopy(self.board), moves)
            if not self._apply_moves(moves, player):
                return self._handle_game_end(opponent, player, f"player{self._get_player_number(opponent)} win")

            if GameRules.in_player1_goal(self.board):
                return self._handle_game_end(self.player2, self.player1, "player2 win")

            if GameRules.in_player2_goal(self.board):
                return self._handle_game_end(self.player1, self.player2, "player1 win")

            if draw:
                self.board.draw()

            player, opponent = opponent, player


    def _initialize_players(self, goes_first):
        self.player1.set_player(0)
        self.player2.set_player(1)
        if goes_first == 1:
            return self.player2, self.player1
        return self.player1, self.player2


    def _apply_moves(self, moves, player):
        player_id = 1 if player == self.player1 else 2
        return self.board.make_moves(moves, player_id)

    def _handle_game_end(self, winner, loser, result_message):
        winner.handle_win()
        loser.handle_loss()
        return self._get_player_number(winner)

    def _get_player_number(self, player):
        return 0 if player == self.player1 else 1
