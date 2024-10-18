#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 15:39:17 2024

@author: theahellen
"""

import pygame, sys
from grid import Grid
from blocks import *

pygame.init()

dark_blue = (44, 44, 127)

screen = pygame.display.set_mode((300, 600)) #setting a 300 width by 600 length pixel screen 
pygame.display.set_caption("Python Tetris") #setting a title

clock = pygame.time.Clock() #setting the frame rate of the game

#printing the game grid (list of lists of cells)
game_grid = Grid() #creates the grid

block = LBlock()


while True: #initialising the game
    for event in pygame.event.get(): #looking through all the possible events
    
        if event.type == pygame.QUIT: #if the user presses the x button on the window it quits the game
            pygame.quit()
            sys.exit()
     
    #Drawing
    screen.fill(dark_blue)
    game_grid.draw(screen)
    block.draw(screen)
    
    pygame.display.update()
    clock.tick(60) #the while loop will run 60 times a second
                   #if we didn't set a frame rate the game would run as fast as possible
                   #leading to inconsistensies in speed
                   
    