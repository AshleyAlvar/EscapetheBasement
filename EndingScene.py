import pygame

class Ending:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
        return None
    
    def draw_ending(self, game):
        self.screen.fill('black')
        text = self.font.render("Congratulations! You've escaped the basement!", True, (255, 255, 255))
        rect = text.get_rect(center=(1466/2, (825/2) - 75))
        self.screen.blit(text, rect)

        text = self.font.render("You took " + str(int(game.tick)) + " seconds to beat the game.", True, (255, 255, 255))
        rect = text.get_rect(center=(1466/2, 825/2))
        self.screen.blit(text, rect)

        text = self.font.render("Press ENTER to back to the menu.", True, (255, 255, 255))
        rect = text.get_rect(center=(1466/2, (825/2) + 75))
        self.screen.blit(text, rect)