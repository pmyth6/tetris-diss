#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 14:45:46 2025

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
        self.model.add(keras.layers.Dense(200, kernel_initializer='RandomNormal', activation="relu"))
        self.model.add(keras.layers.Dense(100, kernel_initializer='RandomNormal', activation="relu"))
        self.model.add(keras.layers.Dense(100, kernel_initializer='RandomNormal', activation="relu"))

        #output layer
        self.model.add(keras.layers.Dense(19, activation="softmax"))
        
        self.hidden1 = self.model.layers[1]
        self.hidden2 = self.model.layers[2]
        self.hidden3 = self.model.layers[3]

        self.optimizer = keras.optimizers.Adam(learning_rate=0.01)
        
        self.moves = ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9",
                     "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0"]

    def loss_fn(self, current_move, probabilities, action_index):
        # Calculate rows with blocks
        rows_with_one = tf.reduce_any(tf.cast(current_move, tf.bool), axis=2)
        self.no_rows = tf.reduce_sum(tf.cast(rows_with_one, tf.float32))
        
        # Calculate base loss based on number of rows
        base_loss = tf.floor((self.no_rows-1.0)/2.0)
        
        # Get the probability of the chosen action
        action_prob = probabilities[0, action_index]
        
        # Combine the losses - we want to maximize action probability when the move is good
        # (i.e., when base_loss is low)
        return base_loss - action_prob/100000
    
    def model_play(self, current_move):
        # Convert input to tensor if it's not already
        current_move = tf.convert_to_tensor(current_move, dtype=tf.float32)
        
        with tf.GradientTape() as tape:
            # Get model predictions
            probabilities = self.model(current_move, training=True)
            
            # Sample action from probabilities
            log_probs = tf.math.log(probabilities)
            action_index = tf.random.categorical(log_probs, 1)[0][0]
            
            # Calculate loss
            loss = self.loss_fn(current_move, probabilities, action_index)
            
        # Calculate gradients
        grads = tape.gradient(loss, self.model.trainable_variables)
        
        # Apply gradients
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        
        # Get the selected action
        action = self.moves[int(action_index)]
        
        # Save to CSV
        self.save_to_csv(current_move, action, self.no_rows, loss)
        
        return action

    def save_to_csv(self, current_move, action, no_rows, loss):
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
                writer.writerow(['grid', 'move', 'number of rows', 'loss'])
        
        row = [current_move.numpy().flatten(), action, no_rows.numpy(), loss.numpy()]
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)