import pygame
import os
from Button import Button

pygame.init()

pygame.display.set_caption("Escape the Basement")
screen = pygame.display.set_mode((1000, 700))
menuTitle = pygame.image.load('EtBTitle.png')
menuBackground = pygame.image.load('basement-2.v1.jpg')

Button_Color = ('red')
Button_hover_color = ('blue')
font = pygame.font.Font(None, 40)
play_button = Button(Button_Color, 300, 400, 200, 100, 'Play', None)
quit_button = Button(Button_Color, 500, 400, 200, 100, 'Quit', None)

def displayMenu():
    pygame.display.flip()
    screen.fill((34, 25, 14))
    screen.blit(menuBackground,(0,0))
    screen.blit(menuTitle, (25, -170))

    play_button.draw(screen, font)
    quit_button.draw(screen, font)
    pygame.display.flip()

running = True
displayMenu()
while running:
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

pygame.quit()
