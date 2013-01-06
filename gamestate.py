# -*- coding: iso-8859-15 -*-
import pygame
from state import *

class GameState(State):
    def update(self):    
        #here comes the game logic, reading the user input, etc
        pass
    def draw(self, screen):
        #here we draw the actual game
        screen.fill((0, 0, 0))
        pygame.display.flip()
