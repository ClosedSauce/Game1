# -*- coding: iso-8859-15 -*-
import pygame
from state import *

class MenuState(State):
    def __init__(self):
        self.bigfont = pygame.font.Font("04B_03__.TTF", 56)
        self.mediumfont = pygame.font.Font("04B_03__.TTF", 24)
        self.selected = 1
        self.setGameResumable(True)
    
    def setGameResumable(self, r):
        self.resumable = r
        if r == False:
            self.menuitems = ["NEW GAME", "QUIT"]
        else:
            self.menuitems = ["RESUME", "NEW GAME", "QUIT"]
    
    def event(self, event):
        key = event.key
        if key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.menuitems)
        if key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.menuitems)
            
    def update(self):
        #here comes the game logic, reading the user input, etc
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        label = self.bigfont.render("MENU", 1, (255,255,0))
        (textW, textH) = self.bigfont.size("MENU")
        posX = screen.get_width() / 2 - textW / 2
        screen.blit(label, (posX, 20))

        for i, text in enumerate(self.menuitems):
            if self.selected == i:
                text = "> " + text + " <"        
            label = self.mediumfont.render(text, 1, (255,255,0))
            (textW, textH) = self.mediumfont.size(text)
            posX = screen.get_width() / 2 - textW / 2
            posY = screen.get_height() / 2 - textH + i * textH
            screen.blit(label, (posX, posY))
        
        pygame.display.flip()
