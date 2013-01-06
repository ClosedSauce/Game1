# -*- coding: iso-8859-15 -*-
import pygame
from state import *

class PauseState(State):
    def update(self):
        #here comes the game logic, reading the user input, etc
        print("This came from the pausestate!")
    def draw(self, screen):
        screen.fill((0, 0, 0))        
        myfont = pygame.font.SysFont("monospace", 32)
        label = myfont.render("Paused!", 1, (255,255,0))
        screen.blit(label, (260, 160))
        pygame.display.flip()
