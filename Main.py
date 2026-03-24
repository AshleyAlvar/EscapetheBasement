import pygame
from Button import Button
from Button import Image_Button
from IntroScene import IntroScene
from GameScene import GameScene

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Escape the Basement")
menuTitle = pygame.image.load('Images/EtBTitle.png')

menuBackground = pygame.image.load('Images/basement-2.v1.jpg')
gameBackground = pygame.image.load('Images/placeholder.jpg') # there will be more on this later

current_background = menuBackground

volume_on = pygame.image.load('Images/volumeon.png').convert_alpha()
volume_off = pygame.image.load('Images/volumeoff.png').convert_alpha()
volumeButton = Image_Button(25, 625, volume_on, 0.15)
current_Volume = volume_on

pygame.mixer.music.load('Audio/universfield-ominous-tones.mp3')
pygame.mixer.music.play(-1, 0.0, 0)

settings_icon = pygame.image.load('Images/settings.png').convert_alpha()
settings_Menu = pygame.image.load('Images/settingMenu.png')
resume_icon = pygame.image.load('Images/Resume.png').convert_alpha()
mainMenu = pygame.image.load('Images/MainMenu.png').convert_alpha()
settingsButton = Image_Button(1200, 1, settings_icon, 0.15)
resumeButton = Image_Button(535, 250, resume_icon, 1)
mainMenuButton = Image_Button(535, 375, mainMenu, 1)


Button_Color = ('red')
Button_hover_color = ('blue')
font = pygame.font.Font(None, 40)
play_button = Button(Button_Color, 430, 400, 200, 100, 'Play', None)
quit_button = Button(Button_Color, 650, 400, 200, 100, 'Quit', None)

def displayMenu(gameState):
    if gameState == "Menu":
        play_button.draw(screen, font)
        quit_button.draw(screen, font)
        volumeButton.draw()
    if gameState == "Game":
        settingsButton.draw()
        volumeButton.draw()

def SettingsMenu():
    screen.blit(settings_Menu, (500, 150))
    resumeButton.draw()
    mainMenuButton.draw()

def updateScreen():
    screen.fill((34, 25, 14))
    screen.blit(current_background,(0,0))
    if current_background == menuBackground:
        screen.blit(menuTitle, (150, -170))

# the screen should only be updated when it needs to be; no need to update it every frame

updateScreen()

running = True
mouseDown = False
musicPaused = False

intro_scene = IntroScene(screen)
game_scene = GameScene(screen)
settingsOpen = False

gameState = "Menu"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    displayMenu(gameState)

    if gameState == "Menu":
        displayMenu(gameState)
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
                    gameState = "Intro"
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

    elif gameState == "Intro":
        intro_scene.draw_intro()
        result = intro_scene.handle_events(event)
        if result is not None:
            game_scene = result
            gameState = "Game"

    elif gameState == "Game":
        # nothing at all for now
        game_scene.draw_game()
        displayMenu(gameState)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouseDown == False and event.button ==1:
                if settingsButton.is_clicked(event.pos):
                    SettingsMenu()
                if resumeButton.is_clicked(event.pos):
                    screen.blit(current_background, (0,0))
                elif mainMenuButton.is_clicked(event.pos):
                    current_background = menuBackground
                    gameState = "Menu"
                    screen.blit(current_background, (0,0))
                    updateScreen()

        if event.type == pygame.MOUSEBUTTONDOWN: # blatant copy and paste; we'll sort this out later
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
            
            mouseDown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
    pygame.display.flip()
pygame.quit()