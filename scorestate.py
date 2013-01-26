# -*- coding: iso-8859-15 -*-
import pygame
from state import *
import pickle

class ScoreState(State):
    maxScores = 10
    scoreFile = 'scores.pkl'
    inputName = ''
    inputScore = 0
    readInput = False
    maxNameLength = 3
    
    def __init__(self):
        self.bigfont = pygame.font.Font("04B_03__.TTF", 56)
        self.mediumfont = pygame.font.Font("04B_03__.TTF", 24)
        self.smallfont = pygame.font.Font("04B_03__.TTF", 16)
        try:
            scoreFile = open(self.scoreFile, 'rb')
            u = pickle.Unpickler(scoreFile)
            self.scores = u.load()
            scoreFile.close()
            print("Read pickle: " + str(self.scores))
        except (pickle.PickleError, EOFError, IOError) as e:
            print("Error reading the pickle file... No scores loaded: " + str(e))
            self.scores = []

    #Returns the position in high scores, 0 if didn't make it to the list, -1 on error
    def checkScorePos(self, score):
        i = 0
        scoresLen = len(self.scores)
        if scoresLen == 0:
            return 1
        for s in self.scores:
            if i < (self.maxScores - 1) and score > s[0]:
                i += 1
                return i
                break
            elif i == (self.maxScores - 1):
                return 0
            else:
                i += 1
        if scoresLen < (self.maxScores):
            return (len(self.scores) + 1)
        else:
            return 0

    #Returns the position in high scores, 0 if didn't make it to the list, -1 on error
    def addScore(self, score, name):
        i = 0
        scoresLen = len(self.scores)
        scoreAdded = False
        if scoresLen == 0:
            self.scores.insert(0, [score, name])
            scoreAdded = True
        else:
            for s in self.scores:
                if i < (self.maxScores - 1) and score > s[0]:
                    self.scores.insert(i, [score, name])
                    scoreAdded = True
                    if len(self.scores) > self.maxScores:
                        self.scores.pop()
                    break
                elif i == (self.maxScores - 1):
                    i = 0
                else:
                    i += 1
        #Special case, score isnt greater than old scores, but there arent yet enough scores to populate the list
        if scoreAdded == False and scoresLen < self.maxScores:
            self.scores.insert(i, [score, name])
        print("Scores: " + str(self.scores))
        
        try:
            output = open(self.scoreFile, 'wb')
            pickle.dump(self.scores, output)
            output.close()
            return i
        except pickle.PickleError:
            print("Error writing the pickle file... No scores written")
            return -1

    def event(self, event):
        if self.readInput == True:
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if len(self.inputName) < self.maxNameLength:
                        self.inputName += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    self.inputName = self.inputName[:-1]
                elif event.key == pygame.K_RETURN:
                    self.readInput = False
                    self.addScore(self.inputScore, self.inputName)
            
    def update(self):
        #here comes the game logic, reading the user input, etc
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        label = self.bigfont.render("HIGH SCORE", 1, (255,255,0))
        (textW, textH) = self.bigfont.size("HIGH SCORE")
        posX = screen.get_width() / 2 - textW / 2
        screen.blit(label, (posX, 20))
        
        if self.readInput == True:
            label = self.smallfont.render("You made it to highscores!", 1, (255,255,0))
            (textW, textH) = self.smallfont.size("You made it to highscores!")
            posX = screen.get_width() / 2 - textW / 2
            screen.blit(label, (posX, 80))

            label = self.smallfont.render("Please input your name:", 1, (255,255,0))
            (textW, textH) = self.smallfont.size("Please input your name:")
            posX = screen.get_width() / 2 - textW / 2
            screen.blit(label, (posX, 120))

            label = self.bigfont.render(self.inputName, 1, (255,255,0))
            (textW, textH) = self.bigfont.size(self.inputName)
            posX = screen.get_width() / 2 - textW / 2
            screen.blit(label, (posX, 160))
        else:
            i = 0
            for s in self.scores:
                i += 1
                label = self.mediumfont.render(str(i) + ". " + s[1] + " - " + str(s[0]), 1, (255,255,0))
                (textW, textH) = self.mediumfont.size(str(i) + ". " + s[1] + " - " + str(s[0]))
                posX = screen.get_width() / 2 - textW / 2
                screen.blit(label, (posX, 80 + i * 20))
                
        pygame.display.flip()
            
    def readUserInput(self):
        self.readInput = True
