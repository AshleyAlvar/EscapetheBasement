import pygame
from Button import Button
from Button import Image_Button

pygame.init()

screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Escape the Basement")
menuTitle = pygame.image.load('EtBTitle.png')
menuBackground = pygame.image.load('basement-2.v1.jpg')

volume_on = pygame.image.load('volumeon.png').convert_alpha()
volume_off = pygame.image.load('volumeoff.png').convert_alpha()
volumeButton = Image_Button(25, 600, volume_on, 0.15)
volumeOff_Button = Image_Button(25, 600, volume_off, 0.15)
current_Volume = volume_on
pygame.mixer.music.load('universfield-ominous-tones.mp3')
pygame.mixer.music.play(-1, 0.0, 0)


Button_Color = ('red')
Button_hover_color = ('blue')
font = pygame.font.Font(None, 40)
play_button = Button(Button_Color, 300, 400, 200, 100, 'Play', None)
quit_button = Button(Button_Color, 500, 400, 200, 100, 'Quit', None)

def displayMenu():
    play_button.draw(screen, font)
    quit_button.draw(screen, font)
    volumeButton.draw()
    pygame.display.flip()

# the screen should only be updated when it needs to be; no need to update it every frame
screen.fill((34, 25, 14))
screen.blit(menuBackground,(0,0))
screen.blit(menuTitle, (25, -170))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
    displayMenu()

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if volumeButton.is_clicked(event.pos):
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

    if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if play_button.is_clicked(event.pos):
                    play_button.action()
                elif quit_button.is_clicked(event.pos):
                    running = False
                    print("Quitting game...")

            while play_button.is_clicked(event.pos):
                print("Play button clicked!")
                break
                

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
