# -*- coding: iso-8859-15 -*-
import state
from gamestate import *
from pausestate import *

class StateManager:
    activeState = 0
    gamestate = 0
    pausestate = 0
    
    def __init__(self):
        self.gamestate = GameState()
        self.pausestate = PauseState()
        self.activeState = self.gamestate
    def getActiveState(self):
        return self.activeState
    def setActiveState(self, state):
        self.activeState = state
