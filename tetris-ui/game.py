#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:50:00 2024

@author: theahellen
"""

#Import packages
import random
#Import grid class and all blocks from the block class
from grid import Grid
from blocks import *

#Define the game class
class Game:
    def __init__(self):
        self.grid = Grid()
        #Initialise the block list
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
    
    #Method to update the score depending on the number of lines cleared or the
    #number of times the user has moved the block down
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        if lines_cleared == 2:
            self.score += 300
        if lines_cleared == 3:
            self.score += 500
        if lines_cleared == 4:
            self.score += 800
        self.score += move_down_points
     
    #Method to retrieve a random block from the list of blocks, if the list is
    #empty it resets the list, every time a block is retrieved it is removed
    #from the list
    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    #Method to move the block left if there is space in the grid
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)
        
    #Method to move the block right if there is space in the grid
    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)
    
    #Method to move the block down if there is space in the grid, once the block
    #has moved down as far as possible it locks into place
    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()
     
    #Method to lock the block into place
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = 1 #when blocks lock 
                                                        #they become light grey
        #The current block becomes the next block
        self.current_block = self.next_block
        #The next block is chosen at random
        self.next_block = self.get_random_block()
        #If when the block is locked a row, or multiple rows, are full, those
        #rows are cleared, the score is updated accordingly and the rows above 
        #are moved down
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        #The grid is printed to the console each time a block is locked into place
        #It is printed after any rows are cleared
        self.grid.print_grid()
        #If the next block doesn't fit inside the grid, the game ends
        if self.block_fits() == False:
            self.game_over = True
    
    #Method to reset the grid
    def reset(self):
        #Set each cell in the grid to 0
        self.grid.reset()
        #Reset the list of blocks, current block and next block
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        #Set the score back to 0
        self.score = 0
        self.game_over = False
      
    #Method to check if the next block fits inside the grid, returns False if the
    #next block doesn't fit and True if it does
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True
     
    #Method to rotate the block 90 degrees clockwise
    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False: 
            self.current_block.undo_rotation()
     
    #Method to rotate the block 90 degrees anticlockwise
    def anti_rotate(self):
        self.current_block.undo_rotation()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.rotate()
    
    #Method to rotate the block by 180 degrees
    def rotate_180(self):
        self.current_block.rotate()
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.rotate()
            self.current_block.rotate()
      
    #Method to check if the current block is within the dimensions of the grid
    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True
    
    #Method to draw the grid, the current block and the next block
    def draw(self, screen):
        self.grid.draw(screen)

        self.current_block.draw(screen, 11, 11)
        
        if self.next_block.id == 3: #centre the I block
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4: #and centre the O block
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)

        
    
        