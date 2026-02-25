import pygame
import os

pygame.init()

pygame.display.set_caption("Escape the Basement")
screen = pygame.display.set_mode((1000, 700))
menuTitle = pygame.image.load('EtBTitle.png')
menuBackground = pygame.image.load('basement-2.v1.jpg')

Button_Color = (100, 100, 100)
Button_hover_color = (150, 150, 150)
font = pygame.font.Font(None, 40)

class Button:
    def __init__(self, color, x, y, width, height, text='', action = None):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen, outline=None):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        
        if self.text != '':
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

play_button = Button(Button_Color, 300, 400, 200, 100, 'Play', None)
quit_button = Button(Button_Color, 500, 400, 200, 100, 'Quit', None)


running = True
while running:
    pygame.display.flip()
    screen.fill((34, 25, 14)
    screen.blit(menuTitle, (25, -170))
    screen.blit(menuBackground,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

    if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if play_button.is_clicked(event.pos):
                    play_button.action()
                elif quit_button.is_clicked(event.pos):
                    running = False
                    print("Quitting game...")

    mouse_pos = pygame.mouse.get_pos()
    if play_button.is_clicked(mouse_pos):
        current_button_color = Button_hover_color
    else:        
        current_button_color = Button_Color

    if quit_button.is_clicked(mouse_pos):
        current_quit_button_color = Button_hover_color
    else:
        current_quit_button_color = Button_Color

    play_button.color = current_button_color
    quit_button.color = current_quit_button_color
    play_button.draw(screen)
    quit_button.draw(screen)
    pygame.display.flip()
            
    

pygame.quit()
