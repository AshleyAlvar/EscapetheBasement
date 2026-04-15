import pygame
from GameScene import Game

class Ending:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.text = "Congratulations! You've escaped the basement! Want to play again? Press Enter to restart."

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return Game(self.screen)
            elif event.type == pygame.QUIT:
                pygame.quit()
                return None

        return None
    
    def draw_ending(self):
        self.screen.fill('black')
        ending_text = self.font.render(self.text, True, (255, 255, 255))
        ending_rect = ending_text.get_rect(center=(640, 360))
        self.screen.blit(ending_text, ending_rect)