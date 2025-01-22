from Players.Player import Player
from Enviroment import *
import numpy as np
from copy import deepcopy
from Enviroment.GameRules import GameRules
from Enviroment.Game import Game
from Players.RandomPlayer import RandomPlayer
from Enviroment.Board import Board
from Players.betterRandom import betterRandomPlayer
from Players.utils import find_lethal


class Node:

    @staticmethod
    def metric(parent,child,c=np.sqrt(2)):
        return child.wins/child.visits+c*np.sqrt(np.log(parent.visits)/child.visits)
    

    def __init__(self,board,my_move=True,parent=None,parent_move=None):
        self.board=board
        self.wins=0
        self.visits=0
        self.parent=parent
        self.parent_move=parent_move
        self.my_move=my_move
        self.children=dict()
        self.valid_moves=GameRules.find_valid_minimoves(board)
        self.untried_actions=deepcopy(self.valid_moves)

    def move(self,move):
        new_board= deepcopy(self.board)
        new_board.fast_make_move(move)
        return self.children.get(move)

    def is_terminal(self):
        #very slow
        return len(self.valid_moves)==0


    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self,c=np.sqrt(2)):
        best_value=-1
        for move,child in self.children.items():
            utc=Node.metric(self,child,c)
            if utc>best_value:
                best_child=child
                best_value=utc
        return best_child

    def selection(self):
        curr = self
        while not curr.is_terminal():
            if not curr.is_fully_expanded():
                return curr.expand()
            else:
                curr=curr.best_child()
        return curr

    def expand(self):
        action = self.untried_actions.pop()
        b= deepcopy(self.board)
        another_move = b.fast_make_move(action)

        if another_move:
            is_my_move=self.my_move
        else:
            is_my_move=not self.my_move
        child = Node(b,my_move=is_my_move,parent=self,parent_move=action)
        self.children[action]=child
        return child
    
    def rollout(self,player):
        b=deepcopy(self.board)
        game = Game(b,betterRandomPlayer(b),betterRandomPlayer(b))
        res = game.start_game(goes_first=(self.my_move==player))
        
        if player==res and (GameRules.in_player1_goal(b) or GameRules.in_player2_goal(b)):
            return 5
        if player==res:
            return 1
        return 0
    def backpropagation(self,result):
        self.visits+=1
        self.wins+=result
        if self.parent:
            self.parent.backpropagation(result) 




class MonteCarloPlayer2(Player):
    def __init__(self,board,playouts=100):
        self.board=board
        self.playouts=playouts
        self.state=Node(deepcopy(board))

    def _update_state(self,moves):
        
        if moves is None:
            return
        for m in moves:
            if m not in self.state.children:
                b= self.state.board
                b.fast_make_move(m)
                self.state=Node(deepcopy(b))
            else:
                self.state=self.state.move(m)
        
    def make_moves(self, board, last_move):
        self._update_state(last_move)
        moves=[]
        lethal = find_lethal(board,self.player)
        if lethal is not None:
            return moves+lethal
        while self.state.my_move:
            for _ in range(self.playouts):
                selected = self.state.selection()
                res = selected.rollout(self.player)
                selected.backpropagation(res)
            best_child = self.state.best_child(c=0)
            moves.append(best_child.parent_move)
            self.state=best_child
            #print(self.state.wins)
        return moves

        

        
        
    