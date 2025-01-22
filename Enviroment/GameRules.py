import numpy as np
from copy import deepcopy
class GameRules:

    number_to_dir = {0: ((-1,0)),1:(-1,1),2:(0,1),3:(1,1),4:(1,0),5:(1,-1),6:(0,-1),7:(-1,-1)}
    dir_to_number = {v: k for k, v in number_to_dir.items()}
    compass_to_dir = {'N':(-1,0),'NE':(-1,1),'E':(0,1),'SE':(1,1),'S':(1,0),'SW':(1,-1),'W':(0,-1),'NW':(-1,-1)}
    

    @staticmethod
    def is_valid_move(board, move):
        next_ball=tuple(a + b for a, b in zip(board.ball, move))
        if (next_ball,board.ball) not in board.board_graph.edges:
            return False
        if board.board_graph.edges[(board.ball,next_ball)]['weight']!=0:
            return False
        if board.ball not in board.touched_fields:
            return False
        return next_ball
    @staticmethod
    def find_valid_minimoves_bitmask(board):
        res = np.zeros(8)
        if GameRules.in_player1_goal(board) or GameRules.in_player2_goal(board):
            return res
        for ind,move in GameRules.number_to_dir.items():
            next_ball=tuple(a + b for a, b in zip(board.ball, move))
            if (next_ball,board.ball) not in board.board_graph.edges:
                continue
            if board.board_graph.edges[(board.ball,next_ball)]['weight']!=0:
                continue
            res[ind]=1
        return res
    @staticmethod
    def in_player1_goal(board):
        return board.ball in board.goals_first
        
        
    @staticmethod
    def in_player2_goal(board):
        return board.ball in board.goals_second
    
    #might have a problem if there are a lot of valid moves
    @staticmethod
    def find_valid_moves(board,max_moves=500):
        valid_moves=[]
        if GameRules.in_player1_goal(board) or GameRules.in_player2_goal(board):
            return valid_moves
        GameRules._explore_moves(board, board.ball, valid_moves, [], max_moves)
        return valid_moves
    
    @staticmethod
    def find_valid_minimoves(board):
        valid_moves=[]
        if GameRules.in_player1_goal(board) or GameRules.in_player2_goal(board):
            return valid_moves
        for neighbor in board.board_graph.neighbors(board.ball):
            if board.board_graph.edges[board.ball, neighbor]['weight'] == 0:
                valid_moves.append(tuple(b - a for a, b in zip(board.ball, neighbor)))
        return valid_moves
    

    @staticmethod
    def _explore_moves(board, current, valid_moves, current_path, max_moves):
        for neighbor in board.board_graph.neighbors(current):
            direction = tuple(b - a for a, b in zip(current, neighbor))

            if not GameRules.is_valid_move(board, direction):
                continue

            if neighbor in board.touched_fields:
                board.board_graph.edges[current, neighbor]['weight'] = -1
                board.ball = neighbor

                GameRules._explore_moves(board, deepcopy(neighbor), valid_moves, current_path + [direction], max_moves-len(valid_moves))

                board.ball = current
                board.board_graph.edges[current, neighbor]['weight'] = 0
            else:
                valid_moves.append(current_path + [direction])

            if max_moves is not None and len(valid_moves) >= max_moves:
                return