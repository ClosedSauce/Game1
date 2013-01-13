# -*- coding: iso-8859-15 -*-
import pygame
from state import *

class ScoreState(State):
    def __init__(self):
        self.bigfont = pygame.font.Font("04B_03__.TTF", 56)
        self.mediumfont = pygame.font.Font("04B_03__.TTF", 24)
    
    def event(self, event):
        pass
            
    def update(self):
        #here comes the game logic, reading the user input, etc
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        label = self.bigfont.render("HIGH SCORE", 1, (255,255,0))
        (textW, textH) = self.bigfont.size("HIGH SCORE")
        posX = screen.get_width() / 2 - textW / 2
        screen.blit(label, (posX, 20))
        
        pygame.display.flip()
