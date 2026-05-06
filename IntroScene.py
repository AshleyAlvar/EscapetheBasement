import pygame
from GameScene import Game

class Intro:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.text = "You are trapped in a dark basement. Ready to escape?"
        self.tick = 0

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.tick = 999
    
    def draw_intro(self, delta):
        self.tick += delta
        self.screen.fill('black')
        lighting = 255
        if self.tick > 3:
            lighting = 255 - (255 * ((self.tick-3)/2))
            if lighting < 0:
                lighting = 0
        intro_text = self.font.render(self.text, True, (lighting, lighting, lighting))
        intro_rect = intro_text.get_rect(center=(1466/2, 825/2))
        self.screen.blit(intro_text, intro_rect)

        if self.tick >= 5.5:
            return True
        return False
        
