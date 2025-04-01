#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:31:01 2024

@author: theahellen
"""

import pygame
import numpy as np
import os
import tensorflow as tf
from PIL import Image
from Dcolors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        #creating a 10x20 grid (list of lists) of 0s:
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()
        # Get a scenario
        self.grid_pass = self.get_scenario()
        self.grid[18:19] = self.grid_pass

    def valid_scenario(self, num1, num2):
        invalid_pairs = {
            1: {1, 11},
            10: {10, 19},
            11: {1, 2, 11, 12},
            19: {9, 10, 18, 19}
        }
        if num1 in invalid_pairs and num2 in invalid_pairs[num1]:
            return False
        if 2 <= num1 < 10 and num2 in {num1, num1 + 9, num1 + 10}:
            return False
        if 12 <= num1 < 19 and num2 in {num1 - 10, num1 - 9, num1 - 1, num1, num1 + 1}:
            return False
        return True

    # Create the scenarios
    def scenario(self, num1, num2):
        grid = np.ones((2, 10))  # Initialize with ones
        for num in [num1, num2]:
            if num <= 10:
                grid[:, num-1] = 0  # Set both rows to 0 at the index
            else:
                grid[1, num-11:num-9] = 0  # Set two consecutive elements in row 1 to 0
        return grid
    
    # Get scenario
    def get_scenario(self):
        # Pick a random scenario
        scenario_num1 = np.random.randint(1, 20)
        scenario_num2 = np.random.randint(1, 20)
        while not self.valid_scenario(scenario_num1,scenario_num2):
            scenario_num1 = np.random.randint(1, 20)
            scenario_num2 = np.random.randint(1, 20)
        grid = self.scenario(scenario_num1,scenario_num2)
        return grid
        
    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()
            
    def get_grid(self):
        #return the grid in the correct format for the model
        grid = self.grid_pass
        tensor = tf.constant(grid, dtype=tf.float32)
        input_tensor = tf.expand_dims(tensor, axis=0)
        return input_tensor
            
    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column>=0 and column < self.num_cols:
            return True
        else:
            return False
        
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False
    
    def is_row_empty(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] != 0:
                return False
        return True
    
    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True
    
    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0
            
    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0
            
    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows-1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed
    
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0
        # Get a scenario
        self.grid_pass = self.get_scenario()
        self.grid[18:19] = self.grid_pass
            
    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column*self.cell_size +11, row*self.cell_size +11, 
                                        self.cell_size -1, self.cell_size -1)
                pygame.draw.rect(screen, self.colors[int(cell_value)], cell_rect)
                