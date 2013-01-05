# -*- coding: iso-8859-15 -*-
import pygame
import time
from statemanager import *

screen = pygame.display.set_mode((640, 400))
running = 1
fps = 60
i = 0

""" Logic for making another step in game """
def update():
    global updateStartTime, updateEndTime, fps, i, activestate, screen
    updateStartTime = time.time()	
    draw(screen)
    i = i + 1
    print("Frame " + str(i))
    activestate.update()
    pygame.time.Clock().tick(fps)

def draw(screen):
    global activestate
    activestate.draw(screen)

while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    statemanager = StateManager()
    activestate = statemanager.getActiveState()
    update()
