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
def updateScreen():
    screen.fill((34, 25, 14))
    screen.blit(menuBackground,(0,0))
    screen.blit(menuTitle, (25, -170))
    pygame.display.flip()

updateScreen()

running = True
mouseDown = False
musicPaused = False

gameState = "Menu"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    displayMenu()

    if gameState == "Menu":
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouseDown == False and event.button == 1:
                # volume button
                if volumeButton.is_clicked(event.pos):
                    musicPaused = not musicPaused
                    updateScreen()
                    if musicPaused == True:
                        volumeButton.new_image(volume_off)
                        pygame.mixer.music.pause()
                        current_Volume = volume_off
                    else:
                        volumeButton.new_image(volume_on)
                        pygame.mixer.music.unpause()
                        current_Volume = volume_on
                # play button
                if play_button.is_clicked(event.pos):
                    gameState = "Game"
                    #play_button.action()
                elif quit_button.is_clicked(event.pos):
                    running = False
                    print("Quitting game...")
                    break
            
            mouseDown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False

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

    elif gameState == "Game":
        # nothing at all for now
        print("test")
        mouse_pos = pygame.mouse.get_pos()

pygame.quit()
