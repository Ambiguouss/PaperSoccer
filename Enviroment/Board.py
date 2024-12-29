import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum
from Enviroment.GameRules import GameRules

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
    Win=1
    Loss=-1


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
        self.board_graph = self.create_graph(n,m)
        self.touched_fields.difference_update(self.goalsfirst)
        self.touched_fields.difference_update(self.goalssecond)

        #print(self.touched_fields)
        
    
    def make_moves(self,moves,player=-1):
        #moved= set()
        if len(moves)==0:
            return False
        for move in moves:
            next_ball= GameRules.is_valid_move(self,move)
            if  next_ball is False:
                return False
            #moved.add(next_ball)
            self.board_graph.add_edge(self.ball,next_ball,weight=player)
            self.ball=next_ball
        if self.ball in self.touched_fields:
            return False
        self.touched_fields.add(self.ball)
        return True
            


    def draw(self):
        plt.figure(figsize=(8, 8))

        # Generate the layout for the nodes (grid positioning)
        pos = {(x, y): (y, -x) for x, y in self.board_graph.nodes}  # Adjusting positions to fit the grid
        edges_weight_2 = [(u, v) for u, v, d in self.board_graph.edges(data=True) if d['weight'] == 2]
        edges_weight_4 = [(u, v) for u, v, d in self.board_graph.edges(data=True) if d['weight'] == 4]
        edges_weight_1 = [(u, v) for u, v, d in self.board_graph.edges(data=True) if d['weight'] == 1]
        edges_weight_0 = [(u, v) for u, v, d in self.board_graph.edges(data=True) if d['weight'] == 0]
        edges_weight_neg = [(u, v) for u, v, d in self.board_graph.edges(data=True) if d['weight'] == -1]

        nx.draw_networkx_nodes(self.board_graph, pos, nodelist=self.goalsfirst,node_size=20, node_color='cyan')
        nx.draw_networkx_nodes(self.board_graph, pos, nodelist=self.goalssecond,node_size=20, node_color='red')
        nx.draw_networkx_nodes(self.board_graph, pos, nodelist=[self.ball],node_size=50, node_color='black')
        nx.draw_networkx_edges(self.board_graph, pos, edgelist=edges_weight_1, width=3, edge_color='blue')  # Bold for weight 1
        nx.draw_networkx_edges(self.board_graph, pos, edgelist=edges_weight_4, width=3, edge_color='green')
        nx.draw_networkx_edges(self.board_graph, pos, edgelist=edges_weight_2, width=3, edge_color='orange')  # Normal for weight 0
        nx.draw_networkx_edges(self.board_graph, pos, edgelist=edges_weight_neg, width=3, edge_color='black')  # Bold for weight 1
        nx.draw_networkx_edges(self.board_graph, pos, edgelist=edges_weight_0, width=1, edge_color='gray')  # Normal for weight 0

        plt.show()

Board()
