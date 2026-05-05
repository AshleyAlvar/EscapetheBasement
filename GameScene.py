import pygame
from Inventory import Hotbar
import Scenes
from copy import deepcopy

game_cursors = {
    "Left" : pygame.cursors.Cursor((50, 50), pygame.image.load("Images/Others/CursorLeft.png").convert_alpha()),
    "Right" : pygame.cursors.Cursor((50, 50), pygame.image.load("Images/Others/CursorRight.png").convert_alpha()),
    "Front" : pygame.cursors.Cursor((50, 50), pygame.image.load("Images/Others/CursorFront.png").convert_alpha()),
    "Back" : pygame.cursors.Cursor((50, 50), pygame.image.load("Images/Others/CursorBack.png").convert_alpha()),
    "Hand" : pygame.SYSTEM_CURSOR_HAND,
    "Default" : pygame.SYSTEM_CURSOR_ARROW,
}

class TipBar:
    def __init__(self, screen):
        self.screen = screen
        self.color = 'black'
        size = 30
        self.rect = pygame.Rect(0,825-size, 1466,size)
        self.text = ''
        self.font = pygame.font.Font(None, 25)
        self.forcedText = None
    
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 0)
        if self.text != '':
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            self.screen.blit(text_surface, text_rect)
    
    def change_text(self, text):
        self.text = text

    def force_text(self, text):
        self.forcedText = self.text
        self.text = text

class Game:

    # class variable
    slot_img = pygame.image.load('Images/hotbarslot.png')
    cursors = game_cursors

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)

        self.scenes = deepcopy(Scenes.Scenes) # upon creation, deep copy the following so that the initial tables do not affected; makes way for when the game resets
        self.items = deepcopy(Scenes.Items)
        self.scene = self.scenes["Front_Room"] # where to draw from specifically

        self.hotbar = Hotbar(445, 680, 75, 7, self.slot_img)
        self.tick = 0
        self.previous = "Front_Room"
        self.has_clicked = []

        self.tipbar = TipBar(screen)

        self.variables = {
            "Placed_Chair" : False,
            "Charger_Plugged" : False,
            "Gold_Locked" : True,
            "Silver_Locked" : True,
            "Vent_Screws" : 4,
            "Powerbox_Screws" : 4,

            "Safe_Locked" : True,
            "Safe_Code" : "",
            
            "Correct_Code1" : "1227",
            "Correct_Code2" : "C36926510_DY",
            "Notes" : pygame.transform.scale(pygame.image.load('Images/Others/Notes.png'), (1466, 825)),

            "Debounce" : 0,
        }

    def draw_game(self, delta : float = 0):
        self.tick += delta
        self.screen.fill((34, 25, 14))
        self.screen.blit(self.scene.background, (0, 0))
        
        for key,overlay in self.scene.overlays.items():
            overlay.draw(self.screen)
        
        for interact in self.scene.interactions:
            if interact.visible == True:
                interact.draw(self.screen)
            if interact.updateOnTick:
                interact.update(self,delta)

        for key,item in self.items.items():
            item.draw(self.screen)

        self.hotbar.draw(self.screen)
        self.tipbar.draw()

        if self.hotbar.selected == "Notes":
            self.screen.blit(self.variables["Notes"], (0, 0))

    def switch_scene(self, scene: str):
        if scene == "Previous":
            scene = self.previous
        if not scene in self.scenes:
            return
        self.scene = self.scenes[scene]
        if self.scene.name != "":
            self.previous = self.scene.name

        for key,item in self.items.items():
            item.visible = False

        self.draw_game()

    #

    def hover(self, pos):
        cursor = ""
        text = ""

        for key,item in self.items.items():
            if not item.collected and item.visible and item.is_clicked(pos):
                cursor = "Hand"
                text = item.name
                break

        if text == "":
            for i, slot in enumerate(self.hotbar.slots):
                if slot.rect.collidepoint(pos) and slot.item is not None:
                    cursor = "Hand"
                    text = slot.item.name
                    break

        if text == "":
            for interact in self.scene.interactions:
                if interact.is_clicked(pos) and interact.enabled == True and interact.cursor != "":
                    if interact.requires_tool == True and self.hotbar.selected == None:
                        continue
                    cursor = interact.cursor
                    text = interact.text
                    break

        if cursor == "":
            pygame.mouse.set_cursor(self.cursors["Default"])
        else:
            pygame.mouse.set_cursor(self.cursors[cursor])

        if self.tipbar.text != text and (self.tipbar.forcedText == None or (text != self.tipbar.forcedText and text != "")):
            self.tipbar.forcedText = None
            self.tipbar.change_text(text)

    def clicked(self, pos):
        print(pos) # debug
        # ITEMS
        clicked = False
        for key,item in self.items.items():
            if not item.collected and item.visible and item.is_clicked(pos):
                if self.hotbar.add_item(item):
                    item.collected = True
                    self.tipbar.force_text("Acquired " + item.name + ".")
                    self.hover(pos)
                clicked = True
                break
            
        if not clicked:
            previous = self.hotbar.selected
            clicked = self.hotbar.handle_click(pos)
            if clicked:
                if self.hotbar.selected != None:
                    self.tipbar.force_text("Selected " + self.hotbar.selected + ".")
                else:
                    self.tipbar.forcedText = None
                    self.tipbar.change_text(previous)
        
        if clicked:
            return
        # INTERACTIONS
        result = None
        for interact in self.scene.interactions:
            if not clicked and interact.is_clicked(pos) and interact.enabled == True:
                if interact.requires_tool == True and self.hotbar.selected == None:
                    continue
                result = interact.mouse_down(self, pos) # sending itself actually works
                self.has_clicked.append(interact)
                clicked = True
                break

    def released(self, pos):
        # INTERACTIONS
        for interact in self.has_clicked: # added so that players wouldn't slide out of said action
            if interact.enabled == True:
                result = interact.mouse_up(self, pos)
                break
        self.has_clicked.clear()
