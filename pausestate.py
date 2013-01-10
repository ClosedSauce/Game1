# -*- coding: iso-8859-15 -*-
import pygame
from state import *

class PauseState(State):
    def __init__(self):
        self.myfont = pygame.font.Font("04B_03__.TTF", 56)
    def update(self):
        #here comes the game logic, reading the user input, etc
        print("This came from the pausestate!")
    def draw(self, screen):
        screen.fill((0, 0, 0))        
        label = self.myfont.render("Paused!", 1, (255,255,0))
        screen.blit(label, (100, 160))
        pygame.display.flip()
