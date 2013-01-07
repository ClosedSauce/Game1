# -*- coding: iso-8859-15 -*-
import pygame
from state import *

class Worm:
    width = 10
    height = 10
    offsetX = 140
    offsetY = 150
    color = 255, 0, 0
    i = 0
    
    def __init__(self):
        self.dirX = 1
        self.dirY = 0

    def update(self):
        self.i = self.i + 1
        if (self.i % 60 == 0):
            self.offsetX = self.offsetX + self.width * self.dirX
            self.offsetY = self.offsetY + self.height * self.dirY
        elif (self.i > 60):
            self.i = self.i - 60
    def draw(self, screen):
        worm = pygame.Rect(self.offsetX, self.offsetY, self.width, self.height)
        screen.fill(self.color, worm)

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

    def __init__(self):
        self.worm = Worm()
    
    def update(self):
        #here comes the game logic, reading the user input, etc
        self.worm.update()
        
    def draw(self, screen):
        #here we draw the actual game
        screen.fill(self.backgroundColor)
        self.initLevel(screen.get_width(), screen.get_height())
        borderArea = pygame.Rect(self.offsetX, self.offsetY, self.width, self.height)
        playArea = pygame.Rect(self.offsetX + self.blockSize, self.offsetY + self.blockSize, self.width - 2 * self.blockSize, self.height - 2 * self.blockSize)
        screen.fill(self.borderColor, borderArea)
        screen.fill(self.playAreaColor, playArea)
        self.worm.draw(screen)
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
