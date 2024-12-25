from Players.Player import Player
from Players.RandomPlayer import RandomPlayer
from Enviroment import *
from Enviroment.Game import Game
from Enviroment.GameRules import GameRules
from Players.MonteCarlo import MonteCarlo
from copy import deepcopy
import json
import numpy as np


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


    def __init__(self,board=None,parent_move=None,parent=None,wins=0,visits=0):
        self.parent=parent
        self.parent_move=parent_move
        self.children=[]
        self.number_of_visits=visits
        self.number_of_wins=wins
        self.board=board
        if board is not None:
            self.valid_moves = GameRules.find_valid_moves(self.board)

    def rollout(self):
        g=deepcopy(self.board)
        game = Game(g,MonteRandomPlayer(g,self),RandomPlayer(g))
        game.start_game()
    
    def is_leaf(self):
        return len(self.children)==0

    def expand(self):
        if self.is_leaf():
            for v in self.valid_moves:
            
                #very bad
                b = deepcopy(self.board)
                b.make_moves(v)
                #for e in v:
                #    e_coord = tuple(a + b for a, b in zip(b.ball, e))
                #    #nie updatuje touched_fields?
                #    b.board_graph.edges[(b.ball,e_coord)]['weight']=-1
                #    b.touched_fields.add(e_coord)
                #    b.ball=e_coord[1]
                self.children.append(Node(b,v,self))

    def selection(self):
        if self.number_of_visits==0:
            self.rollout()
        else:
            self.expand()
            n = np.random.choice(self.children)
            n.selection()

    def to_dict(self):
        return {
            "move": self.parent_move,
            "wins": self.number_of_wins,
            "visits": self.number_of_visits,
            "children": [child.to_dict() for child in self.children]
        }
    @staticmethod
    def from_dict(data):
        move_as_tuple = [tuple(pair) for pair in data["move"]] if data["move"] else None
        node = Node(parent_move=move_as_tuple, wins=data["wins"], visits=data["visits"])
        node.children = [Node.from_dict(child) for child in data["children"]]
        return node


def save_tree(root, filename):
    with open(filename, 'w') as file:
        json.dump(root.to_dict(), file)

def load_tree(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return Node.from_dict(data)


class MonteCarloTrainer():

    def __init__(self,board):
        self.board=board
    
    def train(self):
        tree = Node(self.board)
        for x in range(1000):
            print(x)
            tree.selection()
        

        return tree

    

    #def update_board(self,board):
    #    self.board=board
#
    #def make_moves(self,board):
    #    self.update_board(board)
    #    ball = self.board.ball
    #    move = []
    #    while ball in self.board.touched_fields:
    #        valid_moves=[]
    #        for e in self.board.board_graph.edges(ball):
    #            if self.board.board_graph.edges[e]['weight']==0:
    #                valid_moves.append(e)
    #        if len(valid_moves)==0:
    #            break
    #        move_to_add=valid_moves[np.random.choice(len(valid_moves))]
    #        self.board.board_graph.edges[move_to_add]['weight']=1
    #        move_coord=tuple(b - a for a, b in zip(ball, move_to_add[1]))
    #        move.append(move_coord)
    #        ball = move_to_add[1]
    #    return move


                
