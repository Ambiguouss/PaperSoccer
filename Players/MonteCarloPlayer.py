from Players.Player import Player
from Enviroment import *
import numpy as np
from copy import deepcopy
from Enviroment.GameRules import GameRules
from Enviroment.Game import Game
from Players.RandomPlayer import RandomPlayer

class MonteRandomPlayer(RandomPlayer):
        def __init__(self, board,node):
            super().__init__(board)
            self.node=node
        
        def handle_win(self):
            curr=self.node
            while curr is not None:
                curr.number_of_wins+=1
                curr.number_of_visits+=1
                curr=curr.parent

        def handle_loss(self):
            curr=self.node
            while curr is not None:
                curr.number_of_visits+=1
                curr=curr.parent

class Node:
    def __init__(self,board,parent_move=None,parent=None,wins=0,visits=0,no_moves=100):
        self.parent=parent
        self.parent_move=parent_move
        self.children=[]
        self.number_of_visits=visits
        self.number_of_wins=wins
        self.board=board
        self.valid_moves = GameRules.find_valid_moves(self.board,100)
        self.untried_moves=deepcopy(self.valid_moves)

    def rollout(self):
        g=deepcopy(self.board)
        game = Game(g,MonteRandomPlayer(g,self),RandomPlayer(g))
        game.start_game()
    
    def is_leaf(self):
        return len(self.children)==0

    def expand(self):
        if len(self.untried_moves)>0:
            m = self.untried_moves.pop()
            b = deepcopy(self.board)
            b.make_moves(m)
            k = Node(b,m,self)
            self.children.append(k)
            return k

    def selection(self):
        if len(self.untried_moves)>0:
            child = self.expand()
            child.rollout()
        else:
            max_val=-1
            for child in self.children:
                if child.number_of_visits==0:
                    n=child
                    break
                val = child.number_of_wins/child.number_of_visits+np.sqrt(2)*np.sqrt(np.log(self.number_of_visits)/child.number_of_visits)
                if val>max_val:
                    n=child
                    max_val=val
            n.selection()

class MonteCarloPlayer(Player):

    def __init__(self,board,playouts=10):
        self.board=board
        self.state=Node(deepcopy(board))
        self.playouts=playouts
    
    def update_state(self,last_move):
        if last_move==None:
            return
        for child in self.state.children:
            if child.parent_move==last_move:
                self.state=child
                return
        if last_move in self.state.untried_moves:
            self.state.untried_moves.remove(last_move)
        b = deepcopy(self.state.board)
        b.make_moves(last_move)
        k = Node(b,last_move,self.state)
        self.state.children.append(k)
        self.state=k


    def update_board(self,board):
        self.board=board

    def make_moves(self,board,last_move):
        self.update_state(last_move)
        self.update_board(board)
        for _ in range(self.playouts):
            self.state.selection()
        best_move_value=0
        if len(self.state.children)==0:
            return []
        for child in self.state.children:
            if child.number_of_visits>0 and best_move_value<=child.number_of_wins/child.number_of_visits:
                best_move_value=child.number_of_wins/child.number_of_visits
                best_move=child.parent_move
        self.update_state(best_move)
        self.update_board(board)
        return best_move


                
