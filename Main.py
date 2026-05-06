import pygame
from Button import Button
from Button import Image_Button
from IntroScene import Intro
from GameScene import Game
from Inventory import Hotbar
from Inventory import Item

pygame.init()

screen = pygame.display.set_mode((1466, 825)) # 1280, 720 (changed size again since all the other scenes were in this resolution)
pygame.display.set_caption("Escape the Basement")
gameIcon = pygame.image.load('Images/icon.png')
pygame.display.set_icon(gameIcon)
clock = pygame.time.Clock()

menuBackground = pygame.image.load('Images/MainMenuBg.png')
gameBackground = pygame.image.load('Images/placeholder.jpg') # there will be more on this later

current_background = menuBackground

volume_on = pygame.image.load('Images/volumeon.png').convert_alpha()
volume_off = pygame.image.load('Images/volumeoff.png').convert_alpha()
volumeButton = Image_Button(1466-120, 10, volume_on, 1)
current_Volume = volume_on

mouseClick = pygame.mixer.Sound('Audio/MouseClick.mp3')

settings_icon = pygame.image.load('Images/settings.png').convert_alpha()
settings_Menu = pygame.image.load('Images/settingsmenu.png')
resume_icon = pygame.image.load('Images/Resume.png').convert_alpha()
mainMenu = pygame.image.load('Images/MainMenu.png').convert_alpha()
settingsButton = Image_Button(1466-230, 10, settings_icon, 1)
resumeButton = Image_Button(450, 300, resume_icon, 1)
mainMenuButton = Image_Button(450, 500, mainMenu, 1)

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

    screen.blit(settings_Menu, (0, 0))
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

music_playing = ""
def play_music(str):
    global music_playing
    music_playing = str
    str = f'Audio/{str}.ogg'
    pygame.mixer.music.load(str) # Audio/universfield-ominous-tones.mp3
    pygame.mixer.music.play(-1, 0.0, 0) #TEMPORARY

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

updateScreen()

running = True
mouseDown = False
musicPaused = False
settingsOpen = False
gameState = "Menu"

intro_scene = Intro(screen)
game_scene = Game(screen) # ensure that we can reset this in the future
#ending_scene = Ending(screen)

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
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            elif quit_button.is_clicked(event.pos):
                click()
                running = False
        mouseDown = True
    elif event.type == pygame.MOUSEBUTTONUP:
        mouseDown = False

def handle_game_events(event):
    global mouseDown, settingsOpen, gameState, current_background, game_scene
    if game_scene.Win:
        result = game_scene.win_screen(event)

        global music_playing
        if music_playing != "MenuTheme":
            play_music("MenuTheme")

        if result == "Menu":
            gameState = "Menu"
            current_background = menuBackground

            del game_scene # reset the game
            game_scene = Game(screen)
        return

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
                    
                    del game_scene # reset the game
                    game_scene = Game(screen)
            else:
                game_scene.clicked(event.pos)
        mouseDown = True
    elif event.type == pygame.MOUSEBUTTONUP:
        game_scene.released(event.pos)
        mouseDown = False
    elif event.type == pygame.KEYDOWN:
        game_scene.typed(event)
    elif event.type == pygame.KEYUP:
        game_scene.key_released(event)
    elif event.type == pygame.MOUSEMOTION:
        if settingsButton.is_clicked(event.pos) or volumeButton.is_clicked(event.pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            game_scene.hover(event.pos)

def update_hover():
    if gameState == "Menu":
        mouse_pos = pygame.mouse.get_pos()
        play_button.color = Button_hover_color if play_button.is_clicked(mouse_pos) else Button_Color
        quit_button.color = Button_hover_color if quit_button.is_clicked(mouse_pos) else Button_Color
        
        if play_button.is_clicked(mouse_pos) or quit_button.is_clicked(mouse_pos) or settingsButton.is_clicked(mouse_pos) or volumeButton.is_clicked(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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
        
    if not game_scene.Win:
        updateScreen()
        if gameState == "Intro":
            intro_scene.draw_intro()
        elif gameState == "Game":
            game_scene.draw_game(delta_time_ms / 1000)
        displayMenu()
        update_hover()

    if settingsOpen:
        settingsMenu()

    pygame.display.flip()

pygame.quit()