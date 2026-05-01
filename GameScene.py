import pygame
from Inventory import Hotbar
import Scenes

class Game:

    # class variable
    scenes = Scenes.Scenes
    slot_img = pygame.image.load('Images/hotbarslot.png')

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.scene = self.scenes["Front_Room"] # where to draw from specifically

        self.items = []
        self.hotbar = Hotbar(525, 680, 64, 6, self.slot_img)
        self.variables = dict()
        self.tick = 0

    def draw_game(self, delta : float = 0):
        self.tick += delta
        self.screen.fill((34, 25, 14))
        self.screen.blit(self.scene.background, (0, 0))
        
        for overlay in self.scene.overlays:
            overlay.draw(self.screen)
        
        for interact in self.scene.interactions:
            if interact.visible == True:
                interact.draw(self.screen)

        for item in self.scene.items:
            item.draw(self.screen)

        self.hotbar.draw(self.screen)

    def switch_scene(self, scene: str):
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
                if interact.type == "Transition":
                    self.switch_scene(interact.scene)
                    clicked = True
                break

