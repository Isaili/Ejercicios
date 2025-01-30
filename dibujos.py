import pygame
from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Dibujo en Pygame")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Dibujar un círculo en la ventana
running = True
while running:
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (250, 250), 100)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

pygame.quit()
