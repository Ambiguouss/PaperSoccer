import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum

class Move(Enum):
    N=(-1,0)
    NE=(-1,1)
    E=(0,1)
    SE=(1,1)
    S=(1,0)
    SW=(1,-1)
    W=(0,-1)
    NW=(-1,-1)
    
class GameState(Enum):
    ON=0
    WinFirst=1
    WinSecond=2


class Board:
    def create_graph(self,n,m):
        G = nx.empty_graph()
        G.add_nodes_from([(0,n//2-1),(0,n//2),(0,n//2+1),(m+1,n//2-1),(m+1,n//2),(m+1,n//2+1)])
        G.add_nodes_from((i, j) for i in range(1,m+1) for j in range(n))
        for (i, j) in G.nodes:
            # List all potential neighbors
            neighbors = [
                #(i-1, j-1), (i-1, j), (i-1, j+1),
                (i, j-1), (i, j+1),
                (i+1, j-1), 
                (i+1, j), (i+1, j+1)
            ]
            
            # Add edges if the neighbor node exists in the graph
            for neighbor in neighbors:
                if neighbor in G.nodes:
                    x,y=neighbor
                    if(i in [0, m] and j in [n//2-1, n//2+1] and (n//2-1>y or y>n//2+1) and i!=x):
                        continue
                    elif (i in [0, m+1] and j in [n//2-1, n//2, n//2+1] and i==x) or (1 <= i <= m and (j==y and (j == 0 or j == n-1))):
                        G.add_edge((i, j), neighbor, weight=-1)
                        self.touched_fields.add((i,j))
                        self.touched_fields.add(neighbor)
                    elif(i==x and (i==1 or i==m)and j!=n//2 and y!=n//2):
                        G.add_edge((i, j), neighbor, weight=-1)
                        self.touched_fields.add((i,j))
                        self.touched_fields.add(neighbor)
                    elif(i in [0,m] and j!=n//2 and y==j):
                        #print(i,j,neighbor)
                        G.add_edge((i, j), neighbor, weight=-1)
                        self.touched_fields.add((i,j))
                        self.touched_fields.add(neighbor)
                    else:
                        G.add_edge((i, j), neighbor, weight=0)
        G.remove_edge((m+1,n//2-1),(m,n//2-2))
        G.remove_edge((m+1,n//2+1),(m,n//2+2))
        return G
    
    def __init__(self,n=9,m=11):
        self.n=n
        self.m=m
        self.ball = (m//2+1,n//2)
        self.touched_fields=set()
        self.touched_fields.add(self.ball)
        self.goalsfirst=[(0,self.n//2-1),(0,self.n//2),(0,self.n//2+1)]
        self.goalssecond=[(m+1,n//2-1),(m+1,n//2),(m+1,n//2+1)]
        self.board = self.create_graph(n,m)
        print(self.touched_fields)
        
    
    def make_moves(self,moves,player):
        #move_dict = {Move.N:(-1,0),Move.NE:(-1,1),Move.E:(0,1),Move.SE:(1,1),Move.S:(1,0),Move.SW:(1,-1),Move.W:(0,-1),Move.NW:(-1,-1)}
        moved= set()
        if len(moves)==0:
            raise RuntimeError("must make a move")
        for move in moves:
            move_coord = move
            next_ball=tuple(a + b for a, b in zip(self.ball, move_coord))
            if (next_ball,self.ball) not in self.board.edges:
                raise RuntimeError("invalid move")
            if self.board.edges[(self.ball,next_ball)]['weight']!=0:
                raise RuntimeError("invalid move")
            if self.ball not in self.touched_fields:
                raise RuntimeError("invalid move")
            moved.add(next_ball)
            self.board.add_edge(self.ball,next_ball,weight=player)
            self.ball=next_ball
            if self.ball in self.goalsfirst:
                return GameState.WinSecond
            if self.ball in self.goalssecond:
                return GameState.WinFirst
        if self.ball in self.touched_fields:
            raise RuntimeError("not enought moves")
        self.touched_fields.update(moved)
        #if self.ball in self.goalsfirst:
        #    return GameState.WinSecond
        #if self.ball in self.goalssecond:
        #    return GameState.WinFirst
        return GameState.ON
            


    def draw(self):
        plt.figure(figsize=(8, 8))

        # Generate the layout for the nodes (grid positioning)
        pos = {(x, y): (y, -x) for x, y in self.board.nodes}  # Adjusting positions to fit the grid
        edges_weight_2 = [(u, v) for u, v, d in self.board.edges(data=True) if d['weight'] == 2]
        edges_weight_4 = [(u, v) for u, v, d in self.board.edges(data=True) if d['weight'] == 4]
        edges_weight_1 = [(u, v) for u, v, d in self.board.edges(data=True) if d['weight'] == 1]
        edges_weight_0 = [(u, v) for u, v, d in self.board.edges(data=True) if d['weight'] == 0]
        edges_weight_neg = [(u, v) for u, v, d in self.board.edges(data=True) if d['weight'] == -1]

        nx.draw_networkx_nodes(self.board, pos, nodelist=[self.ball],node_size=50, node_color='black')
        nx.draw_networkx_edges(self.board, pos, edgelist=edges_weight_1, width=3, edge_color='blue')  # Bold for weight 1
        nx.draw_networkx_edges(self.board, pos, edgelist=edges_weight_4, width=3, edge_color='green')
        nx.draw_networkx_edges(self.board, pos, edgelist=edges_weight_2, width=3, edge_color='orange')  # Normal for weight 0
        nx.draw_networkx_edges(self.board, pos, edgelist=edges_weight_neg, width=3, edge_color='black')  # Bold for weight 1
        nx.draw_networkx_edges(self.board, pos, edgelist=edges_weight_0, width=1, edge_color='gray')  # Normal for weight 0

        plt.show()

Board()
