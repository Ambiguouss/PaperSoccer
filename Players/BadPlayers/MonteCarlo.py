from Players.Player import Player
from Enviroment import *
import numpy as np

class MonteCarlo(Player):

    #id=0 when starting, id=1 when going second
    def __init__(self,board,tree,id):
        self.board=board
        self.tree=tree
        self.state=tree
        self.id=id
    
    def update_board(self,board):
        self.board=board

    
    
    def update_state(self,last_move):
        for child in self.state.children:
            if child.parent_move==last_move:
                self.state=child
                #print("update successful")
                return

    def make_moves(self,board,last_move):
        if last_move is not None:
            self.update_state(last_move)
        
        best_move_value=0
        if len(self.state.children)==0:
            return []
        for child in self.state.children:
            if child.number_of_visits>0 and best_move_value<=child.number_of_wins/child.number_of_visits:
                best_move_value=child.number_of_wins/child.number_of_visits
                best_move=child.parent_move
        self.update_state(best_move)
        return best_move

                
