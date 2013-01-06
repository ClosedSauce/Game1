# -*- coding: iso-8859-15 -*-
import pygame
from state import *

class GameState(State):
    backgroundColor = 0, 0, 0
    borderColor = 100, 100, 100
    playAreaColor = 200, 200, 200
    blocks = 23
    blockSize = 0
    offsetX = 0
    offsetY = 0
    width = 0
    height = 0
    
    def update(self):
        #here comes the game logic, reading the user input, etc
        print("This came from the gamestate!")
        
    def draw(self, screen):
        #here we draw the actual game
        screen.fill(self.backgroundColor)
        self.initLevel(screen.get_width(), screen.get_height())
        borderArea = pygame.Rect(self.offsetX, self.offsetY, self.width, self.height)
        playArea = pygame.Rect(self.offsetX + self.blockSize, self.offsetY + self.blockSize, self.width - 2 * self.blockSize, self.height - 2 * self.blockSize)
        screen.fill(self.borderColor, borderArea)
        screen.fill(self.playAreaColor, playArea)
        pygame.display.flip()
        
    def initLevel(self, width, height):
        if(width >= height):
            self.blockSize = height / self.blocks
            self.offsetX = (width - height) / 2
            self.width = height
        else:
            self.blockSize = width / self.blocks
            self.offsetY = (height - width) / 2
            self.width = width
        self.height = self.width
