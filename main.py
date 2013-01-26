# -*- coding: iso-8859-15 -*-
import pygame
import time
from statemanager import *

screen = pygame.display.set_mode((400, 400))
pygame.font.init()
statemanager = StateManager()
running = 1
fps = 60
i = 0

""" Logic for making another step in game """
def update():
    global fps, i, screen, pygame
    updateStartTime = time.time()
    draw(screen)
    i = i + 1
    #print("Frame " + str(i))
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
        activeState = statemanager.getActiveState()
        print("Keydown: " + str(event.key))        
        
        #Disable "Resume" if game is over in gamestate
        if isinstance(activeState, GameState) and statemanager.gamestate.gameover == True:
            statemanager.menustate.setGameResumable(False)
            if statemanager.scorestate.checkScorePos(statemanager.gamestate.score) > 0:
                statemanager.scorestate.inputScore = statemanager.gamestate.score
                statemanager.scorestate.readInput = True
            statemanager.setActiveState(statemanager.scorestate)
        elif event.key == pygame.K_ESCAPE:
            if isinstance(activeState, GameState):
                print("Setting activestate to menustate")
                statemanager.setActiveState(statemanager.menustate)
            elif isinstance(activeState, MenuState) and statemanager.menustate.isGameResumable() == True:
                print("Setting activestate to gamestate")
                statemanager.setActiveState(statemanager.gamestate)
            elif isinstance(activeState, ScoreState):
                print("Setting activestate to menustate")
                statemanager.setActiveState(statemanager.menustate)
        elif event.key == pygame.K_RETURN:
            if isinstance(activeState, MenuState):
                if activeState.menuitems[activeState.selected] == "RESUME":
                    statemanager.setActiveState(statemanager.gamestate)
                if activeState.menuitems[activeState.selected] == "NEW GAME":
                    activeState.selected = 0 #default selected menu item
                    statemanager.gamestate.reset(screen)
                    statemanager.setActiveState(statemanager.gamestate)
                    statemanager.menustate.setGameResumable(True)
                if activeState.menuitems[activeState.selected] == "HIGH SCORE":
                    statemanager.setActiveState(statemanager.scorestate)
                if activeState.menuitems[activeState.selected] == "QUIT":
                    running = 0
            elif isinstance(activeState, ScoreState) and statemanager.scorestate.readInput == False:
                print("Setting activestate to menustate")
                statemanager.setActiveState(statemanager.menustate)
        
        activeState.event(event)
    if running == 0:
        pygame.quit()
    else:
        update()
