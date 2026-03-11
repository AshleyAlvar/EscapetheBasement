import pygame
from Button import Button
from Button import Image_Button
from Game import Game

pygame.init()

screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Escape the Basement")
menuTitle = pygame.image.load('EtBTitle.png')
menuBackground = pygame.image.load('basement-2.v1.jpg')

# Create placeholder volume images since files are missing
volume_on = pygame.Surface((64, 64), pygame.SRCALPHA)
pygame.draw.circle(volume_on, (0, 255, 0), (32, 32), 25)  # Green circle for volume on
volume_off = pygame.Surface((64, 64), pygame.SRCALPHA)
pygame.draw.circle(volume_off, (255, 0, 0), (32, 32), 25)  # Red circle for volume off
volumeButton = Image_Button(25, 600, volume_on, 0.15)
current_Volume = volume_on

# pygame.mixer.music.load('universfield-ominous-tones.mp3')
# pygame.mixer.music.play(-1, 0.0, 0)


Button_Color = ('red')
Button_hover_color = ('blue')
font = pygame.font.Font(None, 40)
play_button = Button(Button_Color, 300, 400, 200, 100, 'Play', None)
quit_button = Button(Button_Color, 500, 400, 200, 100, 'Quit', None)

def draw_intro():
    screen.fill('black')
    intro_text = font.render("You are trapped in a dark basement. Ready to escape?", True, (255, 255, 255))
    intro_rect = intro_text.get_rect(center=(500, 350))
    screen.blit(intro_text, intro_rect)
    pygame.display.flip()

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
                    print("Play button clicked!")
                elif quit_button.is_clicked(event.pos):
                    running = False
                    print("Quitting game...")
                    break

                while play_button.is_clicked(event.pos):
                    draw_intro()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            gameState = "Game"
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

    if gameState == "Game":
        game = Game(screen)
        game.draw_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameState = "Menu"

        mouse_pos = pygame.mouse.get_pos()

pygame.quit()