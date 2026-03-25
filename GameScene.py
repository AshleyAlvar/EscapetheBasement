import pygame
from Inventory import Hotbar
import Interactions

class Scene:
    def __init__(self, /,*, background):
        self.background = background
        self.interactions = {}
        self.items = {}

class Game:

    # class variable
    scenes = {
        "Front_Room" : Scene(
            background = pygame.image.load('Images/placeholder.jpg')
        ),
    }

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.scene = self.scenes["Front_Room"] # where to draw from specifically

        self.hotbar = Hotbar(500, 600, 64, 5)

    def draw_game(self):
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
