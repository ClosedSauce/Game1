# -*- coding: iso-8859-15 -*-
import state
from gamestate import *

class StateManager:
    activeState = 0
    gamestate = 0
    
    def __init__(self):
        self.gamestate = GameState()
        self.activeState = self.gamestate
    def getActiveState(self):
        return self.activeState
    def setCurrentState(self, state):
        self.activeState = state
