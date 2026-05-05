import pygame

# base classes

class Interaction:
    def __init__(self, x, y, x2, y2):
        self.type = "Default"
        self.cursor = ""
        self.text = ""
        self.rect = pygame.Rect(x, y, x2, y2) # rectangle will not show in the game; only used as to detect clicks
        self.visible = False
        self.updateOnTick = False
        self.enabled = True

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def mouse_down(self, game, pos): # ON CLICK
        pass

    def mouse_up(self, game, pos):
        pass

    def update(self, game):
        pass

    def off_scene(self, game):
        pass
    
class Image_Interaction:
    def __init__(self, x, y, image, scale):
        self.type = "Image"
        self.cursor = ""
        self.text = ""
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.scale = scale
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.visible = True
        self.updateOnTick = False
        self.enabled = True
    
    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.is_clicked == False:
                action = True
        
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def new_image(self, screen, *, image):
        width = image.get_width()
        height = image.get_height()
        scale = self.scale
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def mouse_down(self, game, pos):
        pass

    def mouse_up(self, game, pos):
        pass

    def update(self, game):
        pass

    def off_scene(self, game):
        pass

# derived classes

class Text(Interaction):
    def __init__(self, x, y, x2, y2, *, text=""):
        super().__init__(x, y, x2, y2)
        self.type = "Text"
        self.cursor = "Default"
        self.text = text

class Transition(Interaction):
    def __init__(self, x, y, x2, y2, *, scene: str, cursor="Front", text=""):
        super().__init__(x, y, x2, y2)
        self.type = "Transition"
        self.cursor = cursor
        self.text = text
        self.scene = scene # scene name (string)

    def mouse_down(self, game, pos):
        for interaction in game.scene.interactions:
            interaction.off_scene(game)

        game.switch_scene(self.scene)
        game.hover(pos)

class Vent_Transition(Transition):
    def __init__(self, x, y, x2, y2, *, scene: str, cursor="Front", text=""):
        super().__init__(x, y, x2, y2, scene = scene, cursor = cursor, text = text)
    
    def mouse_down(self, game, pos):
        if game.variables["Placed_Chair"] == False:
            if game.hotbar.selected == "Chair" and game.items["Chair"].collected:
                game.tipbar.force_text("Tapping the vent with a chair doesn't seem to do anything. Maybe place it UNDER the vent.")
            else:
                game.tipbar.force_text("Can't seem to reach the vent from this height. You'll need something to stand on to get there.")
        else:
            super().mouse_down(game, pos)

class Cabinet(Interaction):
    def __init__(self, x, y, x2, y2, secondary, overlay, priority):
        super().__init__(x, y, x2, y2)
        self.rect2 = pygame.Rect(secondary[0], secondary[1], secondary[2], secondary[3])
        self.overlay = overlay
        self.priority = priority
        self.cursor = "Hand"
        self.expanded = False

    def is_clicked(self, pos):
        if self.expanded:
            return self.rect2.collidepoint(pos)
        else:
            return self.rect.collidepoint(pos)
    
    def mouse_down(self, game, pos):
        self.expanded = not self.expanded
        for key,overlay in game.scene.overlays.items():
            if key != "Wire":
                if self.expanded:
                    overlay.enabled = (key in self.overlay)
                else:
                    overlay.enabled = (not "_Open" in key)

        self.update(game)
        for cabinet in game.scene.interactions:
            if isinstance(cabinet,Cabinet) and cabinet != self:
                cabinet.expanded = False
                if cabinet.priority > self.priority:
                    cabinet.enabled = not self.expanded  
                cabinet.update(game)      
        game.hover(pos)
    
    def off_scene(self, game):
        self.expanded = False
        self.enabled = True
        for key,overlay in game.scene.overlays.items():
            if key != "Wire":
                overlay.enabled = (not "_Open" in key)

class Item_Cabinet(Cabinet):
    def __init__(self, x, y, x2, y2, secondary, overlay, priority, item):
        super().__init__(x, y, x2, y2, secondary, overlay, priority)
        self.item = item
    
    def update(self, game):
        game.items[self.item].visible = self.expanded

class Silver_Locked_Cabinet(Item_Cabinet):
    def __init__(self, x, y, x2, y2, secondary, overlay, priority, item):
        super().__init__(x, y, x2, y2, secondary, overlay, priority, item)
    
    def mouse_down(self, game, pos):
        if game.hotbar.selected == "Silver Key" and game.items["Silver Key"].collected:
            game.hotbar.remove_item("Silver Key")
            game.variables["Silver_Locked"] = False
            game.tipbar.force_text("Opened locked cabinet.")

            game.scene.overlays["SilverLock"].removed = True
            game.scenes["Front_Room"].overlays["SilverLock"].enabled = False
            game.scenes["Back_Room"].overlays["SilverLock"].enabled = False
            game.scenes["Left_Room"].overlays["SilverLock"].enabled = False

        if game.variables["Silver_Locked"] == True:
            game.tipbar.force_text("This cabinet is locked.")
        else:
            super().mouse_down(game, pos)

class Gold_Locked_Cabinet(Item_Cabinet):
    def __init__(self, x, y, x2, y2, secondary, overlay, priority, item):
        super().__init__(x, y, x2, y2, secondary, overlay, priority, item)
    
    def mouse_down(self, game, pos):
        if game.hotbar.selected == "Gold Key" and game.items["Gold Key"].collected:
            game.hotbar.remove_item("Gold Key")
            game.variables["Gold_Locked"] = False
            game.tipbar.force_text("Opened locked cabinet.")

            game.scene.overlays["GoldLock"].removed = True
            game.scenes["Front_Room"].overlays["GoldLock"].enabled = False
            game.scenes["Right_Room"].overlays["GoldLock"].enabled = False
            game.scenes["Left_Room"].overlays["GoldLock"].enabled = False

        if game.variables["Gold_Locked"] == True:
            game.tipbar.force_text("This cabinet is locked.")
        else:
            super().mouse_down(game, pos)

#

class Item_Interaction(Interaction):
    def __init__(self, x, y, x2, y2, *, cursor="Front", text=""):
        super().__init__(x, y, x2, y2)
        self.type = "Item"
        self.cursor = cursor
        self.text = text # contary to others, this one is important (item)
    
    def mouse_down(self, game, pos):
        item = game.items[self.text]
        if item.collected:
            return False
        if game.hotbar.add_item(item):
            item.collected = True
            self.visible = False
            self.enabled = False
            game.hover(pos)
            game.tipbar.force_text("Acquired " + item.name + ".")
            return True

class SilverKey_Interaction(Item_Interaction):
    def __init__(self, x, y, x2, y2, *, cursor="Front", text=""):
        super().__init__(x, y, x2, y2, cursor=cursor, text=text)

    def mouse_down(self, game, pos):
        confirm = super().mouse_down(game, pos)
        if confirm == True:
            game.scenes["Behind_Cabinet"].change_bg(pygame.image.load('Images/Scenes/Cabinet/BehindCabinet_NoKey.png'))
            game.scenes["Front_Room"].overlays["SilverKey"].enabled = False

class Chair_Interaction(Item_Interaction):
    def __init__(self, x, y, x2, y2, *, cursor="Front", text=""):
        super().__init__(x, y, x2, y2, cursor=cursor, text=text)

    def mouse_down(self, game, pos):
        confirm = super().mouse_down(game, pos)
        if confirm == True:
            game.scenes["Front_Room"].change_bg(pygame.image.load('Images/Scenes/Main1/NoChair.png'))
            game.scenes["Left_Room"].change_bg(pygame.image.load('Images/Scenes/Main4/NoChair.png'))
            game.scenes["Front_Cabinet"].change_bg(pygame.image.load('Images/Scenes/Cabinet/NoChair.png'))
            if game.items["Broom"].collected == True:
                game.scenes["Back_Room"].change_bg(pygame.image.load('Images/Scenes/Main3/NoBroomNChair.png'))
            else:
                game.scenes["Back_Room"].change_bg(pygame.image.load('Images/Scenes/Main3/NoChair.png'))
            game.scenes["Left_Room"].interactions[5].enabled = True # hardcoded

class Broom_Interaction(Item_Interaction):
    def __init__(self, x, y, x2, y2, *, cursor="Front", text=""):
        super().__init__(x, y, x2, y2, cursor=cursor, text=text)

    def mouse_down(self, game, pos):
        confirm = super().mouse_down(game, pos)
        if confirm == True:
            game.scenes["Right_Room"].change_bg(pygame.image.load('Images/Scenes/Main2/NoBroom.png'))
            if game.items["Chair"].collected == True:
                game.scenes["Back_Room"].change_bg(pygame.image.load('Images/Scenes/Main3/NoBroomNChair.png'))
            else:
                game.scenes["Back_Room"].change_bg(pygame.image.load('Images/Scenes/Main3/NoBroom.png'))
            game.scenes["Poster"].overlays["Broom"].enabled = False
            game.scenes["Poster_Removed"].overlays["Broom"].enabled = False

class Chair_Place_Interaction(Interaction):
    def __init__(self, x, y, x2, y2):
        super().__init__(x, y, x2, y2)
        self.type = "Place"
        self.cursor = "Default"
        self.enabled = False
    
    def mouse_down(self, game, pos):
        if game.hotbar.selected == "Chair" and game.items["Chair"].collected:
            game.hotbar.remove_item("Chair")
            game.variables["Placed_Chair"] = True
            game.scenes["Front_Room"].change_bg(pygame.image.load('Images/Scenes/Main1/ChairMoved.png'))
            game.scenes["Left_Room"].change_bg(pygame.image.load('Images/Scenes/Main4/MovedChair.png'))
            game.tipbar.force_text("Placed the chair under the vent. Now we can reach it!")
            self.enabled = False

#

class Safe_Button(Image_Interaction):
    def __init__(self, x, y, image, scale, *, input, clicked_image):
        super().__init__(x, y, image, scale)
        self.cursor = "Hand"
        self.initial_image = image
        self.clicked_image = clicked_image
        self.input = input
    
    def mouse_down(self, game, pos):
        self.new_image(game.screen, image = self.clicked_image)

    def mouse_up(self, game, pos):
        self.new_image(game.screen, image = self.initial_image)