import pygame
from pygame.locals import *

pygame.init()


WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pizarra interactiva")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)

running = True
screen.fill(WHITE)


drawing = False
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            drawing = True  
        elif event.type == MOUSEBUTTONUP:
            drawing = False  
        elif event.type == MOUSEMOTION and drawing:
            #
            pygame.draw.circle(screen, ORANGE,event.pos, 5)

    pygame.display.flip()

pygame.quit()
