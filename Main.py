import pygame
from Button import Button
from Button import Image_Button
from IntroScene import IntroScene
from GameScene import GameScene
from Inventory import Hotbar


pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Escape the Basement")
menuTitle = pygame.image.load('Images/EtBTitle.png')
clock = pygame.time.Clock()

menuBackground = pygame.image.load('Images/basement-2.v1.jpg')
gameBackground = pygame.image.load('Images/placeholder.jpg') # there will be more on this later

current_background = menuBackground

volume_on = pygame.image.load('Images/volumeon.png').convert_alpha()
volume_off = pygame.image.load('Images/volumeoff.png').convert_alpha()
volumeButton = Image_Button(25, 625, volume_on, 0.15)
current_Volume = volume_on

pygame.mixer.music.load('Audio/universfield-ominous-tones.mp3')
pygame.mixer.music.play(-1, 0.0, 0)
mouseClick = pygame.mixer.Sound('Audio/MouseClick.mp3')

settings_icon = pygame.image.load('Images/settings.png').convert_alpha()
settings_Menu = pygame.image.load('Images/settingMenu.png')
resume_icon = pygame.image.load('Images/Resume.png').convert_alpha()
mainMenu = pygame.image.load('Images/MainMenu.png').convert_alpha()
settingsButton = Image_Button(1200, 1, settings_icon, 0.15)
resumeButton = Image_Button(535, 250, resume_icon, 1)
mainMenuButton = Image_Button(535, 375, mainMenu, 1)

slot_img = pygame.image.load('Images/hotbarslot.png')

Button_Color = ('red')
Button_hover_color = ('blue')
font = pygame.font.Font(None, 40)
play_button = Button(Button_Color, 430, 400, 200, 100, 'Play', None)
quit_button = Button(Button_Color, 650, 400, 200, 100, 'Quit', None)

hotbar = Hotbar(500, 600, 64, 5, slot_img)

def Click():
    mouseClick.play()

def SettingsMenu():
    overlay = pygame.Surface((1280, 720))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    screen.blit(settings_Menu, (500, 150))
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
        hotbar.draw(screen)

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
        screen.blit(menuTitle, (150, -170))

updateScreen()

running = True
mouseDown = False
musicPaused = False
settingsOpen = False
gameState = "Menu"

intro_scene = IntroScene(screen)
game_scene = GameScene(screen)

gameState = "Menu"

# handlers

def handle_menu_events(event):
    global running, mouseDown, gameState, current_background
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if not mouseDown:
            if volumeButton.is_clicked(event.pos):
                Click()
                toggle_volume()
            elif play_button.is_clicked(event.pos):
                Click()
                gameState = "Game"
                current_background = gameBackground
            elif quit_button.is_clicked(event.pos):
                Click()
                running = False
        mouseDown = True
    elif event.type == pygame.MOUSEBUTTONUP:
        mouseDown = False

def handle_game_events(event):
    global mouseDown, settingsOpen, gameState, current_background
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if not mouseDown:
            if volumeButton.is_clicked(event.pos):
                Click()
                toggle_volume()
            elif settingsButton.is_clicked(event.pos):
                Click()
                settingsOpen = not settingsOpen
            elif settingsOpen:
                if resumeButton.is_clicked(event.pos):
                    Click()
                    settingsOpen = False
                elif mainMenuButton.is_clicked(event.pos):
                    Click()
                    settingsOpen = False
                    gameState = "Menu"
                    current_background = menuBackground
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if gameState == "Menu":
            handle_menu_events(event)
        elif gameState == "Game":
            handle_game_events(event)
   
    updateScreen()
    if gameState == "Intro":
        intro_scene.draw_intro()
    elif gameState == "Game":
        game_scene.draw_game()

    displayMenu()
    update_hover()

    if settingsOpen:
        SettingsMenu()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()