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
        #load model
        self.model = keras.models.load_model("100neuronlayersLR00081LeakyReLuB.keras",
                                             custom_objects={'LeakyReLU': tf.keras.layers.LeakyReLU})
        
        self.moves = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0",
                      "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"]
    
    def model_play(self, current_move):
        # Convert input to tensor if it's not already
        current_move = tf.convert_to_tensor(current_move, dtype=tf.float32)

        # Get model probabilities
        # Move 1
        probabilities1 = self.model(current_move, training=False)
        move_index1 = tf.argmax(probabilities1, axis=1)

        grid = grid.numpy()[0]
        if int(move_index1)+1 <= 10:
            grid[:, int(move_index1)] = 1  # Set both rows to 0 at the index
        else:
            grid[1, int(move_index1)-10:int(move_index1)-8] = 1 
        grid = tf.convert_to_tensor(grid, dtype=tf.float32)  # Convert back to TensorFlow tensor
        grid = tf.expand_dims(grid, axis=0)

        # Move 2
        probabilities2 = self.model(grid, training=False)
        move_index2 = tf.argmax(probabilities2, axis=1)
        
        # Get the selected actions
        action1 = self.moves[int(move_index1)]
        action2 = self.moves[int(move_index2)]
        action = [action1, action2]
        
        return action