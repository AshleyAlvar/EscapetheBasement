import pygame
from Inventory import Hotbar

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.background = pygame.image.load('Images/placeholder.jpg')

        self.hotbar = Hotbar(500, 600, 64, 5)
        self.items = []

    def draw_game(self):
        self.screen.fill((34, 25, 14))
        self.screen.blit(self.background, (0, 0))

        for item in self.items:
            item.draw(self.screen)

        self.hotbar.draw(self.screen)
