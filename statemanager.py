# -*- coding: iso-8859-15 -*-
import state
from gamestate import *
from menustate import *
from scorestate import *

class StateManager:
    activeState = 0
    gamestate = 0
    menustate = 0
    scorestate = 0
    
    def __init__(self):
        self.gamestate = GameState()
        self.menustate = MenuState()
        self.scorestate = ScoreState()
        self.activeState = self.menustate
    
    def getActiveState(self):
        return self.activeState
    
    def setActiveState(self, state):
        self.activeState = state
