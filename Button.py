import pygame

class Button:
    def __init__(self, color, x, y, width, height, text='', action = None):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen, font, outline=None):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        
        if self.text != '':
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
