#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:32:12 2024

@author: theahellen
"""

from Dblock import Block
from Dposition import Position

class DBlock(Block): #this class is now a child of the block class using inheritance
    def __init__(self):
        super().__init__(id = 1)
        self.cells = {
            0: [Position(0, 0), Position(0, 1)],
            1: [Position(0, 1), Position(1, 1)],
            2: [Position(1, 0), Position(1, 1)],
            3: [Position(0, 0), Position(1, 0)]
        }
        self.move(0, 4) #so that the block spawns in the middle of the grid
        

    