import pygame
from GameScene import GameScene

class IntroScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.text = "You are trapped in a dark basement. Ready to escape?"

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return GameScene(self.screen)
        return None
    
    def draw_intro(self):
        self.screen.fill('black')
        intro_text = self.font.render(self.text, True, (255, 255, 255))
        intro_rect = intro_text.get_rect(center=(640, 360))
        self.screen.blit(intro_text, intro_rect)

