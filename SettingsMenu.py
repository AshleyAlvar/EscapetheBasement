import pygame

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.background = pygame.image.load('Images/placeholder.jpg')

    def draw_game(self):
        self.screen.fill((34, 25, 14))
        self.screen.blit(self.background, (0, 0))