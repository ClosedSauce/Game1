# -*- coding: iso-8859-15 -*-
import pygame
import copy
from state import *
from collections import deque

""" Everything in the gamearea is a block """
class Block:
    blockSize = 10
    offsetX = 30
    offsetY = 150
    dirX = 1
    dirY = 0
    color = 255, 0, 0
    i = 0
    
    def __init__(self):
        self.dirX = 1
        self.dirY = 0

    def update(self):
        pass
    
    def draw(self, screen):
        block = pygame.Rect(self.offsetX, self.offsetY, self.blockSize, self.blockSize)
        screen.fill(self.color, block)

""" Worm is basically a stack of blocks, which player can control """
class Worm:
    i = 0
    startOffsetX = 4 #in blocks
    startOffsetY = 4 #in blocks
    blockSize = 0
    
    def __init__(self):
        initialBlock = Block()
        secondBlock = Block()
        thirdBlock = Block()
        fourthBlock = Block()        
        self.blocks = deque([fourthBlock, thirdBlock, secondBlock, initialBlock])

    """ Should only be called at the very start of the game """ 
    def setBlocksize(self, blockSize): #@todo rename to more corresponding
        self.blockSize = blockSize
        for i, b in enumerate(self.blocks):
            b.blockSize = blockSize
            #We want to make the coordinates to the closest "block"
            b.offsetX = self.startOffsetX * blockSize + i * blockSize
            b.offsetY = self.startOffsetY * blockSize
            
    
    def event(self, event):
        print("Keyevent at gamestate!")
        if event.key == pygame.K_w:
            self.blocks[len(self.blocks)-1].dirY = -1
            self.blocks[len(self.blocks)-1].dirX = 0
        if event.key == pygame.K_s:
            self.blocks[len(self.blocks)-1].dirY = 1
            self.blocks[len(self.blocks)-1].dirX = 0
        if event.key == pygame.K_a:
            self.blocks[len(self.blocks)-1].dirX = -1
            self.blocks[len(self.blocks)-1].dirY = 0
        if event.key == pygame.K_d:
            self.blocks[len(self.blocks)-1].dirX = 1
            self.blocks[len(self.blocks)-1].dirY = 0
    
    def update(self):
        self.i = self.i + 1
        
        if (self.i % 10 == 0): #Updating every 60th frame
            newBlock = copy.deepcopy(self.blocks[len(self.blocks)-1])
            newBlock.offsetX = newBlock.offsetX + newBlock.blockSize * newBlock.dirX
            newBlock.offsetY = newBlock.offsetY + newBlock.blockSize * newBlock.dirY
            print("NewX: " + str(newBlock.offsetX) + " , len: " + str(len(self.blocks)))
            self.blocks.append(newBlock)
            self.blocks.popleft()

    def draw(self, screen):
        for i, b in enumerate(self.blocks):
            b.draw(screen)

class GameState(State):
    backgroundColor = 0, 0, 0
    borderColor = 100, 100, 100
    playAreaColor = 200, 200, 200
    
    """ Game is made of certain sized blocks. Sort of "big pixels" """
    #from how many blocks the game area is formed from
    blocks = 20
    
    #following are just for initing the variables
    #blockSize will be calculated based on drawarea width and heigh (and amount of blocks)
    blockSize = 0 
    offsetX = 0
    offsetY = 0
    width = 0
    height = 0

    def __init__(self):
        self.worm = Worm()

    def event(self, event):
        self.worm.event(event)
    
    def update(self):
        #here comes the game logic, reading the user input, etc
        self.worm.update()
        
    def draw(self, screen):
        #here we draw the actual game
        screen.fill(self.backgroundColor)
        self.initLevel(screen.get_width(), screen.get_height()) #@todo this should be done only once
        borderArea = pygame.Rect(self.offsetX, self.offsetY, self.width, self.height)
        playArea = pygame.Rect(self.offsetX + self.blockSize, self.offsetY + self.blockSize, self.width - 2 * self.blockSize, self.height - 2 * self.blockSize)
        screen.fill(self.borderColor, borderArea)
        screen.fill(self.playAreaColor, playArea)
        
        self.worm.draw(screen)
        
        pygame.display.flip()
        
    def initLevel(self, width, height):
        if (width >= height):
            self.blockSize = height / self.blocks
            self.offsetX = (width - height) / 2
            self.width = height
        else:
            self.blockSize = width / self.blocks
            self.offsetY = (height - width) / 2
            self.width = width
        self.height = self.width
        
        if (self.worm.blockSize == 0):
            self.worm.setBlocksize(self.blockSize)
