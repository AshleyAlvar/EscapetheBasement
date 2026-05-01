import pygame
from Button import Button
from Button import Image_Button
from IntroScene import Intro
from GameScene import Game
from Inventory import Hotbar
from Inventory import Item
from EndingScene import Ending


pygame.init()

screen = pygame.display.set_mode((1466, 825)) # 1280, 720 (changed size again since all the other scenes were in this resolution)
pygame.display.set_caption("Escape the Basement")
menuTitle = pygame.image.load('Images/EtBTitle.png')
clock = pygame.time.Clock()

menuBackground = pygame.image.load('Images/basement-2.v1.jpg')
gameBackground = pygame.image.load('Images/placeholder.jpg') # there will be more on this later

current_background = menuBackground

volume_on = pygame.image.load('Images/volumeon.png').convert_alpha()
volume_off = pygame.image.load('Images/volumeoff.png').convert_alpha()
volumeButton = Image_Button(20, 825-120, volume_on, 1)
current_Volume = volume_on

mouseClick = pygame.mixer.Sound('Audio/MouseClick.mp3')

settings_icon = pygame.image.load('Images/settings.png').convert_alpha()
settings_Menu = pygame.image.load('Images/settingMenu.png')
resume_icon = pygame.image.load('Images/Resume.png').convert_alpha()
mainMenu = pygame.image.load('Images/MainMenu.png').convert_alpha()
settingsButton = Image_Button(1466-120, 10, settings_icon, 1)
resumeButton = Image_Button(608, 300, resume_icon, 1)
mainMenuButton = Image_Button(608, 425, mainMenu, 1)

slot_img = pygame.image.load('Images/hotbarslot.png')

Button_Color = ('red')
Button_hover_color = ('blue')
font = pygame.font.Font(None, 40)
play_button = Button(Button_Color, 633-125, 460, 200, 100, 'Play', None)
quit_button = Button(Button_Color, 633+125, 460, 200, 100, 'Quit', None)

#hotbar = Hotbar(525, 680, 64, 6, slot_img)
frame_rate = 60

"""
key_img = pygame.image.load('Images/key.png')
key = Item(600, 500, key_img, 0.2)
key2 = Item(800, 500, key_img, 0.2)
"""

game_items = [] # [key, key2]

def click():
    mouseClick.play()

def settingsMenu():
    overlay = pygame.Surface((1466, 825))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    screen.blit(settings_Menu, (573, 200))
    resumeButton.draw()
    mainMenuButton.draw()

def displayMenu():
    if gameState == "Menu":
        play_button.draw(screen, font)
        quit_button.draw(screen, font)
        volumeButton.draw()

    elif gameState == "Game":
        settingsButton.draw()
        volumeButton.draw()
        #hotbar.draw(screen)
        #key.draw(screen)
        #key2.draw(screen)

def play_music(str):
    str = f'Audio/{str}.ogg'
    pygame.mixer.music.load(str) # Audio/universfield-ominous-tones.mp3
    pygame.mixer.music.play(-1, 0.0, 0)

play_music("MenuTheme")

def toggle_volume():
    global musicPaused, current_Volume

    musicPaused = not musicPaused

    if musicPaused:
        volumeButton.new_image(volume_off)
        pygame.mixer.music.pause()
        current_Volume = volume_off
    else:
        volumeButton.new_image(volume_on)
        pygame.mixer.music.unpause()
        current_Volume = volume_on


def updateScreen():
    screen.fill((34, 25, 14))
    screen.blit(current_background,(0,0))
    if current_background == menuBackground:
        screen.blit(menuTitle, (0, -125))

updateScreen()

running = True
mouseDown = False
musicPaused = False
settingsOpen = False
gameState = "Menu"

intro_scene = Intro(screen)
game_scene = Game(screen)
ending_scene = Ending(screen)
gameState = "Menu"

# handlers

def handle_menu_events(event):
    global running, mouseDown, gameState, current_background
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if not mouseDown:
            if volumeButton.is_clicked(event.pos):
                click()
                toggle_volume()
            elif play_button.is_clicked(event.pos):
                click()
                gameState = "Game" # Intro
                play_music("GameTheme")
            elif quit_button.is_clicked(event.pos):
                click()
                running = False
        mouseDown = True
    elif event.type == pygame.MOUSEBUTTONUP:
        mouseDown = False

def handle_game_events(event):
    global mouseDown, settingsOpen, gameState, current_background
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if not mouseDown:
            if volumeButton.is_clicked(event.pos):
                click()
                toggle_volume()
            elif settingsButton.is_clicked(event.pos):
                click()
                settingsOpen = not settingsOpen
            elif settingsOpen:
                if resumeButton.is_clicked(event.pos):
                    click()
                    settingsOpen = False
                elif mainMenuButton.is_clicked(event.pos):
                    click()
                    settingsOpen = False
                    gameState = "Menu"
                    current_background = menuBackground
                    play_music("MenuTheme")
            else:
                game_scene.clicked(event.pos)
        mouseDown = True
    elif event.type == pygame.MOUSEBUTTONUP:
        mouseDown = False

def update_hover():
    mouse_pos = pygame.mouse.get_pos()
    if gameState == "Menu":
        play_button.color = Button_hover_color if play_button.is_clicked(mouse_pos) else Button_Color
        quit_button.color = Button_hover_color if quit_button.is_clicked(mouse_pos) else Button_Color

# main loop

while running:
    delta_time_ms = clock.tick(frame_rate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if gameState == "Menu":
            handle_menu_events(event)
        elif gameState == "Intro":
            new_scene = intro_scene.handle_events(event)
            if new_scene:
                game_scene = new_scene
                gameState = "Game"
                current_background = gameBackground
        elif gameState == "Game":
            handle_game_events(event)
        elif gameState == "Ending":
            new_scene = ending_scene.handle_events(event)
            if new_scene:
                game_scene = new_scene
                gameState = "Game"
                current_background = gameBackground
         
    updateScreen()
    if gameState == "Intro":
        intro_scene.draw_intro()
    elif gameState == "Game":
        game_scene.draw_game(delta_time_ms / 1000)
    elif gameState == "Ending":
        ending_scene.draw_ending()


    displayMenu()
    update_hover()

    if settingsOpen:
        settingsMenu()

    pygame.display.flip()

pygame.quit()