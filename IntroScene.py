import pygame
pygame.init()
screen = pygame.display.set_mode((1000, 700))
font = pygame.font.Font(None, 40)

def draw_intro():
    screen.fill('black')
    intro_text = font.render("You are trapped in a dark basement. Ready to escape?", True, (255, 255, 255))
    intro_rect = intro_text.get_rect(center=(640, 360))
    screen.blit(intro_text, intro_rect)
    pygame.display.flip()

