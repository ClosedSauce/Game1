# -*- coding: iso-8859-15 -*-
import state

class StateManager:
    activeState = 0

    def __init__(self):
        pass #tähän luonnit gamestatelle ynnä muille
    def getCurrentState(self):
        return self.activeState
    def setCurrentState(self, state):
        self.activeState = state
