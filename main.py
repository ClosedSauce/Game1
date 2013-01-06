# -*- coding: iso-8859-15 -*-
import pygame
import time
from statemanager import *

screen = pygame.display.set_mode((640, 400))
pygame.font.init()
statemanager = StateManager()
running = 1
fps = 100
i = 0

""" Logic for making another step in game """
def update():
    global fps, i, screen, pygame
    updateStartTime = time.time()
    
    draw(screen)
    
    i = i + 1
    print("Frame " + str(i))
       
    
    statemanager.getActiveState().update()
    pygame.time.Clock().tick(fps)

def draw(screen):
    global activestate
    statemanager.getActiveState().draw(screen)

while running:
    
    event = pygame.event.poll()
    
    if event.type == pygame.QUIT:
        running = 0
    elif event.type == pygame.KEYDOWN:
        print("Keydown: " + str(event.key))
        if event.key == pygame.K_p:
            if (isinstance(statemanager.getActiveState(), GameState)):
                print("Setting activestate to pausestate")
                statemanager.setActiveState(statemanager.pausestate)
            elif (isinstance(statemanager.getActiveState(), PauseState)):
                print("Setting activestate to gamestate")
                statemanager.setActiveState(statemanager.gamestate)

    update()
