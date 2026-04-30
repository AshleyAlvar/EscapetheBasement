import pygame
from Inventory import Hotbar
import Interactions

class Scene:
    def __init__(self, /,*, background):
        self.background = background
        self.interactions = []
        self.items = []

    def change_bg(self, background):
        self.background = background

class Game:

    # class variable
    scenes = {
        "Front_Room" : Scene(
            background = pygame.image.load('Images/Scenes/Main1/Scene.png')
        ),
        "Right_Room" : Scene(
            background = pygame.image.load('Images/Scenes/Main2/Scene.png')
        ),
        "Back_Room" : Scene(
            background = pygame.image.load('Images/Scenes/Main3/Scene.png')
        ),
        "Left_Room" : Scene(
            background = pygame.image.load('Images/Scenes/Main4/Scene.png')
        ),
    }
    slot_img = pygame.image.load('Images/hotbarslot.png')

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.scene = self.scenes["Front_Room"] # where to draw from specifically

        self.items = []
        self.hotbar = Hotbar(525, 680, 64, 6, self.slot_img)
        self.variables = dict()

    def draw_game(self, delta_time_ms):
        self.screen.fill((34, 25, 14))
        self.screen.blit(self.scene.background, (0, 0))

        for item in self.scene.items:
            item.draw(self.screen)

        self.hotbar.draw(self.screen)

    def switch_scene(self, scene):
        if not scene in self.scenes:
            return
        self.scene = self.scenes[scene]
        self.draw_game()

    #

    def clicked(self, pos):
        print(pos) # debug
        # ITEMS
        clicked = False
        for item in self.items:
            if not item.collected and item.is_clicked(pos):
                if self.hotbar.add_item(item):
                    item.collected = True
                clicked = True
                break
        if not clicked:
            self.hotbar.handle_click(pos)
        # INTERACTIONS
        for interact in self.scene.interactions:
            if not clicked and interact.is_clicked(pos):
                print("clicked!")
                if interact.type == "Transition":
                    scene = self.scenes[interact.scene]
                    self.switch_scene(scene)
                    clicked = True
                break

