import pygame
wall_color = ('brown')
floor_color = ('gray')

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.wall_color = wall_color
        self.floor_color = floor_color
        
    def draw_game(self):
        self.screen.fill(self.floor_color)
        pygame.draw.rect(self.screen, self.wall_color, (0, 0, 1000, 700), 10)
        pygame.display.flip()
