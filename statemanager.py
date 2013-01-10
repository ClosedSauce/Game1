# -*- coding: iso-8859-15 -*-
import state
from gamestate import *
from menustate import *

class StateManager:
    activeState = 0
    gamestate = 0
    menustate = 0
    
    def __init__(self):
        self.gamestate = GameState()
        self.menustate = MenuState()
        self.activeState = self.menustate
    
    def getActiveState(self):
        return self.activeState
    
    def setActiveState(self, state):
        self.activeState = state
