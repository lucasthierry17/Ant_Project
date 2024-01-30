import numpy as np
import pygame

FPS = 200
clock = pygame.time.Clock()
pygame.init()

width = 500
height = 400
initial_alpha = 255
array = np.full((width, height), initial_alpha, dtype=np.uint8)

screen = pygame.display.set_mode([width, height])
surface = pygame.Surface((width, height), pygame.SRCALPHA)

liste = []
for i in range(100):
    for j in range(100):
        liste.append((i, j))

running = True

def drawing():
    surface.fill((0, 0, 255, 0))  # Fill with transparent blue
    for i, j in liste:
        array[i, j] = max(array[i, j] - 1, 0)
        pygame.draw.rect(surface, (0, 0, 255, array[i, j]), [i, j, 1, 1])

    screen.fill((0, 0, 0))
    screen.blit(surface, (0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    drawing()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
