import pygame
import time

screen = pygame.display.set_mode((640, 400))
running = 1
fps = 60
i = 0

""" Logic for making another step in game """
def update():
    global updateStartTime, updateEndTime, fps, i
    updateStartTime = time.time()	
    draw()
    i = i + 1
    print("Frame " + str(i))
    pygame.time.Clock().tick(fps)

def draw():
    global screen
    screen.fill((0, 0, 0))
    pygame.display.flip()

while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    update()
