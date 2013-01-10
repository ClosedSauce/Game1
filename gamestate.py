# -*- coding: iso-8859-15 -*-
import pygame
import copy
from state import *
from collections import deque

""" Everything in the gamearea is a block """
class Block:
    blockSize = 10
    #coordinates in blocks
    x = 0
    y = 0
    dirX = 1
    dirY = 0
    color = 155, 155, 155
    i = 0
    
    
    def __init__(self):
        self.dirX = 1
        self.dirY = 0

    def update(self):
        pass
    
    def draw(self, screen):
        block = pygame.Rect(self.x * self.blockSize, self.y * self.blockSize, self.blockSize, self.blockSize)
        screen.fill(self.color, block)
       

""" Worm is basically a stack of blocks, which player can control """
class Worm:
    i = 0
    startOffsetX = 4 #in blocks
    startOffsetY = 4 #in blocks
    blockSize = 0
    
    def __init__(self, gamestate):
        initialBlock = Block()
        secondBlock = Block()
        thirdBlock = Block()
        fourthBlock = Block()        
        self.blocks = deque([fourthBlock, thirdBlock, secondBlock, initialBlock])
        self.gamestate = gamestate
        self.keyQueue = deque([]) #stores keypresses, so they can be chained

    """ Should only be called at the very start of the game """
    def initWorld(self, blockSize):
        self.blockSize = blockSize
        for i, b in enumerate(self.blocks):
            b.blockSize = blockSize
            #We want to make the coordinates to the closest "block"
            b.x = self.startOffsetX  + i
            b.y = self.startOffsetY
            
    
    def event(self, event):
        print("Keyevent at gamestate!")
        self.keyQueue.append(event.key)        
    
    def update(self):
        self.i = self.i + 1
        
        if self.i % 10 == 0: #Updating every 60th frame
            
            #take a one keypress from the keyQueue, leave the rest
            if len(self.keyQueue) > 0:
                key = self.keyQueue.popleft()
                b = self.blocks[len(self.blocks)-1]
                b2 = self.blocks[len(self.blocks)-2] #to check that cannot move to previous block "inside itself"
                if key == pygame.K_w and (b.y - 1 <> b2.y or b.x <> b2.x):
                    b.dirY = -1
                    b.dirX = 0
                if key == pygame.K_s and (b.y + 1 <> b2.y or b.x <> b2.x):
                    b.dirY = 1
                    b.dirX = 0
                if key == pygame.K_a and (b.y <> b2.y or b.x - 1 <> b2.x):
                    b.dirX = -1
                    b.dirY = 0
                if key == pygame.K_d and (b.y <> b2.y or b.x + 1 <> b2.x):
                    b.dirX = 1
                    b.dirY = 0
            
            newBlock = copy.deepcopy(self.blocks[len(self.blocks)-1])
            newBlock.x = newBlock.x + newBlock.dirX
            newBlock.y = newBlock.y + newBlock.dirY
            
            if (self.gamestate.checkFreeSpace(newBlock.x, newBlock.y) == False):
                print("Collision!")
            else:
                print("NewX: " + str(newBlock.x) + " , len: " + str(len(self.blocks)))
                self.blocks.append(newBlock)
                self.blocks.popleft()

    def draw(self, screen):
        for i, b in enumerate(self.blocks):
            b.draw(screen)

class GameState(State):
    backgroundColor = 0, 0, 0
    borderColor = 0, 0, 0
    playAreaColor = 75, 75, 75
    
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
        self.worm = Worm(self)
        self.smallFont = pygame.font.Font("04B_03__.TTF", 16)

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

        label = self.smallFont.render("Score: ", 1, (155,155,155))
        screen.blit(label, (self.blockSize, 3))
        
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
            self.worm.initWorld(self.blockSize)

    #true if current coordinates are "free to be moved at", false if used, either by worm or walls
    # x and y are block, so actual coordinates are x * blockSize
    # Assumes that border is 1 block in width
    def checkFreeSpace(self, x, y):
        if (x <= 0 or y <= 0 or x * self.blockSize >= (self.width - self.blockSize) or y * self.blockSize >= (self.height - self.blockSize)):
            return False
        for i, b in enumerate(self.worm.blocks):
            if (b.x == x and b.y == y):
                return False
        return True
