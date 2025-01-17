#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 17:12:53 2025

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np

class Model:
    def __init__(self):
        #create a sequential model
        self.model = keras.models.Sequential()

        #first layer: converts each grid (20x10 array) to a 1d array
        self.model.add(keras.layers.Flatten(input_shape=[20, 10]))

        #dense layers
        self.model.add(keras.layers.Dense(200, kernel_initializer='RandomNormal', activation="relu"))
        self.model.add(keras.layers.Dense(100, kernel_initializer='RandomNormal', activation="relu"))
        self.model.add(keras.layers.Dense(100, kernel_initializer='RandomNormal', activation="relu"))

        #output layer
        self.model.add(keras.layers.Dense(19, activation="softmax"))
        
        self.hidden1 = self.model.layers[1]
        self.hidden2 = self.model.layers[2]
        self.hidden3 = self.model.layers[3]

        #print the weights of each layer
        weights, biases = self.hidden1.get_weights()
        print(weights)
        weights, biases = self.hidden2.get_weights()
        print(weights)
        weights, biases = self.hidden3.get_weights()
        print(weights)

        self.model.compile()
        
    def model_play(self, current_move):
        next_move = self.model.predict(current_move)
        print(next_move)
        next_move = np.argmax(next_move, axis=1)
        moves = ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9",
                 "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0"]
        return moves[next_move[0]]


