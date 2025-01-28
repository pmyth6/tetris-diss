#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 12:14:24 2025

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import csv

class Model:
    def __init__(self):
        #create a sequential model
        self.model = keras.models.Sequential()

        #input layer to define the input shape
        self.model.add(keras.Input(shape=(20, 10)))

        #convert each grid (20x10 array) to a 1D array
        self.model.add(keras.layers.Flatten())

        #dense layers
        self.model.add(keras.layers.Dense(100, kernel_initializer='RandomNormal', activation="relu"))
        self.model.add(keras.layers.Dense(50, kernel_initializer='RandomNormal', activation="relu"))
        self.model.add(keras.layers.Dense(50, kernel_initializer='RandomNormal', activation="relu"))

        #output layer
        self.model.add(keras.layers.Dense(19, activation="softmax"))
        
        
        
        self.hidden1 = self.model.layers[1]
        self.hidden2 = self.model.layers[2]
        self.hidden3 = self.model.layers[3]

        self.optimizer = keras.optimizers.Adam(learning_rate=0.1)
        
        self.moves = ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9",
                     "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0"]
        
        self.current_grid = []
        
        self.row = 0
        
        self.previous_action = "h5"
    
    def model_play(self, current_move, score, game_no):
        # Convert input to tensor if it's not already
        current_move = tf.convert_to_tensor(current_move, dtype=tf.float32)
        
        self.current_grid = current_move
        
        with tf.GradientTape() as tape:
            # Get model predictions
            probabilities = self.model(current_move, training=True)
            
            # Sample action from probabilities
            log_probs = tf.math.log(probabilities)
            action_index = tf.random.categorical(log_probs, 1)[0][0]
            
            # Get the selected action
            action = self.moves[int(action_index)]
            
            # Calculate loss
            loss = self.loss_fn(current_move, probabilities, action_index, action, score)
            
        # Calculate gradients
        grads = tape.gradient(loss, self.model.trainable_variables)
        
        # Apply gradients
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        
        # Save to CSV
        self.save_to_csv(current_move, action, self.row, loss, game_no, score)
        
        # Set current move as previous move for future use
        self.previous_action = action
        
        return action
    
    def loss_fn(self, current_move, probabilities, action_index, action, score):
        # Get the number of the row the block will be placed in
        self.row = self.calculate_row_placement(action)
        
        # Calculate base loss based on the row
        #base_loss = tf.floor((self.row-1.0)/2.0)
        
        # Calculate base loss as the squared row placement
        base_loss = self.row**2
        
        # Get the probability of the chosen action
        action_prob = probabilities[0, action_index]
        
        # If the model makes the same move twice - punish it
        repeat_loss = 0
        if self.previous_action == action:
            repeat_loss = 10

        return -(base_loss - action_prob/100000 + repeat_loss - score)
    
    def calculate_row_placement(self, action):
        # 1 1
        if action[0] == "h":
            col = int(action[1])
            col -= 1 # Zero based indexing
            
            row = 19
            while self.current_grid[0, 20-row, col] == 0 and self.current_grid[0, 20-row, col+1] == 0:
                row -= 1
                if row == 0:
                    break
            
        # 1
        # 1
        if action[0] == "v":
            col = int(action[1])
            if col == 0:
                col = 10
            col -=1 # Zero based indexing
            
            row = 19
            while self.current_grid[0, 20-row, col] == 0 and self.current_grid[0, 20-row-1, col] == 0:
                row -= 1
                if row == 0:
                    break
                
        return row+1
    
    '''
    def calculate_gap(self, action):
        gap = 0
        row = self.row-1 # Zero based indexing
        col = int(action[1])
        col -= 1 # Zero based indexing
        
        if action[0] == "h":
            while self.current_grid[0, 20-row, col] == 0 and self.current_grid[0, 20-row, col+1] == 0:
                row -= 1
                if row == 0:
                    break
            
        
        return gap
    '''
            

    def save_to_csv(self, current_move, action, no_rows, loss, no_games, score):
        filename = "log.csv"
        
        file_exists = False
        try:
            with open(filename, 'r'):
                file_exists = True
        except FileNotFoundError:
            pass
        
        if not file_exists:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['grid', 'move', 'row placement', 'loss', 'score', 
                                 'game no.', 'weights layer 1', 'weights layer 2', 'weights layer 3'])
        
        weights1, biases1 = self.hidden1.get_weights()
        weights2, biases2 = self.hidden2.get_weights()
        weights3, biases3 = self.hidden3.get_weights()
        
        row = [current_move.numpy().flatten(), action, no_rows, loss.numpy(), 
               score, no_games, weights1, weights2, weights3]
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)