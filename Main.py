import pygame
import os

pygame.init()

pygame.display.set_caption("Escape the Basement")
screen = pygame.display.set_mode((1000, 700))
menuTitle = pygame.image.load('EtBTitle.png')

running = True
while running:
    pygame.display.flip()
    screen.fill((34, 25, 14))
    screen.blit(menuTitle, (25, -170))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()
