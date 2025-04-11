#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:30:17 2024

@author: theahellen
"""

from Dgrid import Grid
from Dblocks import *
from basic_dmodel2 import Model
from Dcolors import Colors
import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [DBlock()]
        self.current_block = DBlock()
        self.next_block = DBlock()
        self.game_over = False
        self.score = 0
        self.model = Model()
        self.game_no = 0
        self.screen = pygame.display.set_mode((320, 620))

        #get grid
        input_grid = self.grid.get_grid()
        #get moves
        next_move = self.model.model_play(input_grid)
        #interpret and execute move
        move_1 = list(enumerate(next_move[0]))
        self.move_2 = list(enumerate(next_move[1]))
        print(move_1[0][1],move_1[1][1])
        print(self.move_2[0][1],self.move_2[1][1])
        if move_1[0][1] == "h":
            if move_1[1][1] == "1" and self.game_over == False:
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
            if move_1[1][1] == "2":
                self.move_left()
                self.move_left()
                self.move_left()
            if move_1[1][1] == "3":
                self.move_left()
                self.move_left()
            if move_1[1][1] == "4":
                self.move_left()
            if move_1[1][1] == "6":
                self.move_right()
            if move_1[1][1] == "7":
                self.move_right()
                self.move_right()
            if move_1[1][1] == "8":
                self.move_right()
                self.move_right()
                self.move_right()
            if move_1[1][1] == "9":
                self.move_right()
                self.move_right()
                self.move_right()
                self.move_right()
        if move_1[0][1] == "v" and self.game_over == False:
            self.rotate()
            if move_1[1][1] == "1":
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
            if move_1[1][1] == "2":
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
            if move_1[1][1] == "3":
                self.move_left()
                self.move_left()
                self.move_left()
            if move_1[1][1] == "4":
                self.move_left()
                self.move_left()
            if move_1[1][1] == "5":
                self.move_left()
            if move_1[1][1] == "7":
                self.move_right()
            if move_1[1][1] == "8":
                self.move_right()
                self.move_right()
            if move_1[1][1] == "9":
                self.move_right()
                self.move_right()
                self.move_right()
            if move_1[1][1] == "0":
                self.move_right()
                self.move_right()
                self.move_right()
                self.move_right()
        
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
    
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)
        
    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)
        
    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()
            
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = 1

        self.current_block = self.next_block
        self.next_block = DBlock()

        # Draw the new block before applying second move
        self.update()
        self.draw()
        pygame.time.delay(100)

        if (self.grid.is_row_full(19) and self.grid.is_row_full(18)) or not self.grid.is_row_empty(17):
            self.game_over = True
            self.reset()
            return

        def move_horizontal(direction, times):
            for _ in range(times):
                if direction == "left":
                    self.move_left()
                elif direction == "right":
                    self.move_right()

        if self.game_over is False:
            if self.move_2[0][1] == "h":
                move_map = {
                    "1": 4, "2": 3, "3": 2, "4": 1,
                    "6": 1, "7": 2, "8": 3, "9": 4
                }
                val = self.move_2[1][1]
                if val in move_map:
                    if val in ["1", "2", "3", "4"]:
                        move_horizontal("left", move_map[val])
                    elif val in ["6", "7", "8", "9"]:
                        move_horizontal("right", move_map[val])

            if self.move_2[0][1] == "v":
                self.rotate()
                move_map = {
                    "1": 5, "2": 4, "3": 3, "4": 2, "5": 1,
                    "7": 1, "8": 2, "9": 3, "0": 4
                }
                val = self.move_2[1][1]
                if val in move_map:
                    if val in ["1", "2", "3", "4", "5"]:
                        move_horizontal("left", move_map[val])
                    elif val in ["7", "8", "9", "0"]:
                        move_horizontal("right", move_map[val])

        # Final update and draw after move_2
        self.update()
        self.draw()
        pygame.time.delay(100)
        
            
    def reset(self):
        self.grid.reset()
        self.blocks = [DBlock()]
        self.current_block = DBlock()
        self.next_block = DBlock()
        self.score = 0
        self.game_no += 1
        self.game_over = False

        #get grid
        input_grid = self.grid.get_grid()
        #get moves
        next_move = self.model.model_play(input_grid)
        #interpret and execute move
        move_1 = list(enumerate(next_move[0]))
        self.move_2 = list(enumerate(next_move[1]))
        print(move_1[0][1],move_1[1][1])
        print(self.move_2[0][1],self.move_2[1][1])
        if move_1[0][1] == "h":
            if move_1[1][1] == "1" and self.game_over == False:
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
            if move_1[1][1] == "2":
                self.move_left()
                self.move_left()
                self.move_left()
            if move_1[1][1] == "3":
                self.move_left()
                self.move_left()
            if move_1[1][1] == "4":
                self.move_left()
            if move_1[1][1] == "6":
                self.move_right()
            if move_1[1][1] == "7":
                self.move_right()
                self.move_right()
            if move_1[1][1] == "8":
                self.move_right()
                self.move_right()
                self.move_right()
            if move_1[1][1] == "9":
                self.move_right()
                self.move_right()
                self.move_right()
                self.move_right()
        if move_1[0][1] == "v" and self.game_over == False:
            self.rotate()
            if move_1[1][1] == "1":
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
            if move_1[1][1] == "2":
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
            if move_1[1][1] == "3":
                self.move_left()
                self.move_left()
                self.move_left()
            if move_1[1][1] == "4":
                self.move_left()
                self.move_left()
            if move_1[1][1] == "5":
                self.move_left()
            if move_1[1][1] == "7":
                self.move_right()
            if move_1[1][1] == "8":
                self.move_right()
                self.move_right()
            if move_1[1][1] == "9":
                self.move_right()
                self.move_right()
                self.move_right()
            if move_1[1][1] == "0":
                self.move_right()
                self.move_right()
                self.move_right()
                self.move_right()
            
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        self.model.model.save('model.keras')
        return True
            
    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False: 
            self.current_block.undo_rotation()
     
    def anti_rotate(self):
        self.current_block.undo_rotation()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.rotate()
            
    def rotate_180(self):
        self.current_block.rotate()
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.rotate()
            self.current_block.rotate()
        
    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def draw(self):
        self.screen.fill(Colors.dark_blue)  # or your background color
        self.grid.draw(self.screen)
        self.current_block.draw(self.screen, 11, 11)
        pygame.display.update()

    def update(self):
        self.move_down()
        if self.block_inside() == False:
            self.current_block.move_up()
            self.lock_block()
        
        
        
    
        