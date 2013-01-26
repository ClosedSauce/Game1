# -*- coding: iso-8859-15 -*-
import pygame
import copy
import random
from state import *
from collections import deque

""" Everything in the gamearea is a block """
class Block:
    blockSize = 10
    
    #coordinates in blocks
    x = 5
    y = 5
    
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

class Food:
    
    def __init__(self):
        self.block = Block()

    def setPos(self, x, y):
        self.block.x = x
        self.block.y = y

    def getPos(self):
        return (self.block.x, self.block.y)
    
    def update(self):
        pass

    def draw(self, screen):
        self.block.draw(screen)

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
        self.hp = 1
    
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
        
        if self.i % 15 == 0: #Updating every Nth frame
            self.i = 0
            #take a one keypress from the keyQueue, leave the rest
            if len(self.keyQueue) > 0:
                key = self.keyQueue.popleft()
                b = self.blocks[len(self.blocks)-1]
                b2 = self.blocks[len(self.blocks)-2] #to check that cannot move to previous block "inside itself"
                if key == pygame.K_UP and (b.y - 1 <> b2.y or b.x <> b2.x):
                    b.dirY = -1
                    b.dirX = 0
                if key == pygame.K_DOWN and (b.y + 1 <> b2.y or b.x <> b2.x):
                    b.dirY = 1
                    b.dirX = 0
                if key == pygame.K_LEFT and (b.y <> b2.y or b.x - 1 <> b2.x):
                    b.dirX = -1
                    b.dirY = 0
                if key == pygame.K_RIGHT and (b.y <> b2.y or b.x + 1 <> b2.x):
                    b.dirX = 1
                    b.dirY = 0
            
            newBlock = copy.deepcopy(self.blocks[len(self.blocks)-1])
            newBlock.x = newBlock.x + newBlock.dirX
            newBlock.y = newBlock.y + newBlock.dirY

            collision = self.gamestate.checkCollision(newBlock.x, newBlock.y)            
            if collision == 1:
                print("Collision with wall!")
                self.hp -= 1
            #following special checks are so that worm can "go around", following its own tail
            elif collision == 2 and (newBlock.x <> self.blocks[0].x or newBlock.y <> self.blocks[0].y):
                print("Collision with worm!")
                self.hp -= 1
                #print("Collision, new coords " + str(newBlock.x) + ", " + str(newBlock.y) + " vs " + str(self.blocks[0].x) + ", " + str(self.blocks[0].y))
            elif collision == 3:
                print("Omnomnom")
                self.blocks.append(newBlock)
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
    gameover = False
    
    """ Game is made of certain sized blocks. Sort of "big pixels" """
    #from how many blocks the game area is formed from
    blocks = 16
    
    #following are just for initing the variables
    #blockSize will be calculated based on drawarea width and heigh (and amount of blocks)
    blockSize = 0 
    offsetX = 0
    offsetY = 0
    width = 0
    height = 0

    score = 0

    def randomizeFoodPos(self):
        e = 0
        while True:
            newFoodX = random.randint(1, self.blocks - 2)
            random.jumpahead(random.randint(1, self.blocks - 2))
            newFoodY = random.randint(1, self.blocks - 2)
            e += 1
            print("Randomizing " + str(e))
            if self.checkCollision(newFoodX, newFoodY) == 0 or e > 500:
                break
        self.food.setPos(newFoodX, newFoodY)
    
    def __init__(self):
        self.smallFont = pygame.font.Font("04B_03__.TTF", 16)
        self.bigfont = pygame.font.Font("04B_03__.TTF", 56)
        
    def reset(self, screen):
        self.worm = Worm(self)
        self.score = 0
        self.food = Food()
        self.food.block.color = (200, 200, 0)        
        self.initLevel(screen.get_width(), screen.get_height())
        self.randomizeFoodPos()
        self.gameover = False
        
    def event(self, event):
        if self.worm.hp > 0:
            self.worm.event(event)
    
    def update(self):
        #here comes the game logic, reading the user input, etc
        if self.worm.hp > 0:
            self.worm.update()
            self.food.update()
        else:
            self.gameover = True
        
    def draw(self, screen):
        #here we draw the actual game
        screen.fill(self.backgroundColor)
        
        borderArea = pygame.Rect(self.offsetX, self.offsetY, self.width, self.height)
        playArea = pygame.Rect(self.offsetX + self.blockSize, self.offsetY + self.blockSize, self.width - 2 * self.blockSize, self.height - 2 * self.blockSize)
        screen.fill(self.borderColor, borderArea)
        screen.fill(self.playAreaColor, playArea)

        label = self.smallFont.render("Score: " + str(self.score), 1, (155,155,155))
        (labelW, labelH) = self.smallFont.size("Score: " + str(self.score))
        screen.blit(label, (self.blockSize, self.blockSize / 2 - labelH / 2))
        
        self.worm.draw(screen)
        self.food.draw(screen)

        if self.gameover == True:
            #We create a partial transparent fill to the gamescreen
            dimSurface = pygame.Surface((screen.get_width(), screen.get_height()))
            dimSurface.set_alpha(192)
            dimSurface.fill((0, 0, 0))
            screen.blit(dimSurface, (0,0))
            
            label = self.bigfont.render("GAME OVER", 1, (255,255,0))
            (textW, textH) = self.bigfont.size("GAME OVER")
            posX = screen.get_width() / 2 - textW / 2
            screen.blit(label, (posX, 20))

            label = self.smallFont.render("Press any key to continue", 1, (255,255,0))
            (textW, textH) = self.smallFont.size("Press ESC to enter menu")
            posX = screen.get_width() / 2 - textW / 2
            screen.blit(label, (posX, screen.get_height() / 1.25))

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

        self.food.block.blockSize = self.blockSize        
        self.randomizeFoodPos()
        
        if (self.worm.blockSize == 0):
            self.worm.initWorld(self.blockSize)

    # x and y are block, so actual coordinates are x * blockSize
    # Assumes that border is 1 block in width
    # returns 0 = free, 1 = wall, 2 = worm, 3 = food    
    def checkCollision(self, x, y):
        if (x <= 0 or y <= 0 or x * self.blockSize >= (self.width - self.blockSize) or y * self.blockSize >= (self.height - self.blockSize)):
            return 1
        for i, b in enumerate(self.worm.blocks):
            if b.x == x and b.y == y:
                return 2
        (foodX, foodY) = self.food.getPos()
        if (x == foodX and y == foodY):
            self.randomizeFoodPos()
            self.score += 1
            return 3
        return 0
    
