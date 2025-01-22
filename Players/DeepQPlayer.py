import random
import keras
from Players.Player import Player
from Enviroment import *
import numpy as np
from copy import deepcopy
from Enviroment.GameRules import GameRules
from Enviroment.Game import Game
from Players.RandomPlayer import RandomPlayer
from Players.betterRandom import betterRandomPlayer
from Players.utils import find_lethal,test
import tensorflow as tf



class DeepQPlayer(Player):
    
    number_to_dir = {0: ((-1,0)),1:(-1,1),2:(0,1),3:(1,1),4:(1,0),5:(1,-1),6:(0,-1),7:(-1,-1)}
    dir_to_number = {v: k for k, v in number_to_dir.items()}

    def update_target(self):
        self.target_network.set_weights(self.main_network.get_weights()) 


    def __init__(self,board,learning_rate=0.001,epoch_number=100,eps_greedy=0.02,gamma=0.1):
        self.board=deepcopy(board)
        action_shape=8
        state_shape=690
        self.epoch_number=epoch_number
        self.eps_greedy=eps_greedy
        self.gamma=gamma
        init = tf.keras.initializers.HeUniform()
        self.main_network = keras.Sequential()
        self.main_network.add(keras.layers.Dense(128, input_shape = (state_shape,),activation='relu',kernel_initializer=init))
        self.main_network.add(keras.layers.Dense(64, activation='relu',kernel_initializer=init))
        self.main_network.add(keras.layers.Dense(action_shape, activation='linear',kernel_initializer=init))
        self.main_network.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate), metrics=['accuracy'])
        self.target_network = deepcopy(self.main_network)
    

    def train_step(self,replay_buffer):
        if len(replay_buffer)<1280:
            return
        random_index = np.random.choice(len(replay_buffer))
        state,action,reward,next_state,my_turn,done = replay_buffer[random_index]

        


        
        if my_turn:
            next_Qs=self.target_network(next_state)[0]
            next_Q = np.max(next_Qs)
            target = tf.constant(reward+self.gamma*next_Q*(1-done))
        else:
            #assuming that reversed <=> looking from opponents perspective
            next_Qs=self.target_network(next_state[::-1])[0]
            next_Q = np.min(next_Qs)
            target = tf.constant(reward+self.gamma*(-next_Q)*(1-done))

        

        with tf.GradientTape() as tape:
            Q = self.main_network(state)[0]
            target_idx = GameRules.dir_to_number[action]

            indices = [[target_idx]]
            updates=[target]
            
            newQ = tf.tensor_scatter_nd_update(Q, indices,updates)
            loss = tf.keras.losses.MeanSquaredError().call(newQ,Q)
        # Compute gradients
        trainable_vars = self.main_network.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)
        # Update weights
        self.main_network.optimizer.apply_gradients(zip(gradients, trainable_vars))



    def choose_move(self,state,player,epoch):
        eps= self.eps_greedy/(max(1,epoch/5000)) #change this and eps next
        
        q_values = self.main_network(state.to_vector(player))[0].numpy()
        valid_bitmask = GameRules.find_valid_minimoves_bitmask(state)
        q_values[valid_bitmask == 0] = -np.inf
        if np.sum(valid_bitmask)==0:
            return None
        probabilities = np.full(valid_bitmask.shape,eps)*valid_bitmask
        best_move= np.argmax(q_values)
        probabilities[best_move]= 1-(np.sum(valid_bitmask)-1)*eps
        probabilities=probabilities/np.sum(probabilities)  
        
        choosen = np.random.choice(8,p=probabilities)
        
        if probabilities[choosen]==0:
            GameRules.number_to_dir[best_move]
        return GameRules.number_to_dir[choosen]

    def fit(self):
        #he is the player1
        replay_buffer = []
        for epoch in range(self.epoch_number):
            print(epoch)
            state = deepcopy(self.board) #To be changed
            done = False
            player=0
            while not done:
                action = self.choose_move(state,player,epoch)
                reward = 0
                done = False
                if action is None:
                    reward=-1
                    done = True
                else:
                    next_state = deepcopy(state)
                    #maybe i should add another random action after this
                    my_turn = next_state.fast_make_move(action)
                    #use target network for adversary move??
                    if GameRules.in_player1_goal(next_state):
                        reward=-1 if player==0 else 1
                        done = True
                    elif GameRules.in_player2_goal(next_state): 
                        reward=1 if player==0 else -1
                        done=True
                    elif len(GameRules.find_valid_minimoves(next_state))==0 and my_turn:
                        reward=-1
                        done=True
                replay_buffer.append((state.to_vector(player),action,reward,next_state.to_vector(player),my_turn,done))
                if len(replay_buffer)>10000:
                    replay_buffer.pop(0)
                self.train_step(replay_buffer)
                state=next_state
            if epoch%1000 == 0:
                self.update_target()
            if epoch%1000==0:
                f = open("logs8", "a")
                f.write(f"{epoch}/{self.epoch_number}: {test(self,betterRandomPlayer(deepcopy(self.board)))}\n")
                f.close()


        
            
    def make_mini_move(self,board):
        q_values = self.main_network(board.to_vector())[0].numpy()
        bitmask = GameRules.find_valid_minimoves_bitmask(board)
        q_values[bitmask == 0] = -np.inf
        best_move= np.argmax(q_values)
        return GameRules.number_to_dir[best_move]



    def make_moves(self,board,last_move):
        moves = []
        while True:
            lethal = find_lethal(board,self.player)
            if lethal is not None:
                return moves+lethal
            mini_move = self.make_mini_move(board)
            moves.append(mini_move)
            my_turn = board.fast_make_move(mini_move)
            if not my_turn:
                return moves




                
