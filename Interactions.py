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
        
        self.requires_tool = False

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def mouse_down(self, game, pos): # ON CLICK
        pass

    def mouse_up(self, game, pos):
        pass

    def update(self, game, delta=0):
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

        self.requires_tool = False
    
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

    def update(self, game, delta=0):
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

class Laptop_Transition(Transition):
    def __init__(self, x, y, x2, y2, *, scene: str, cursor="Front", text=""):
        super().__init__(x, y, x2, y2, scene = scene, cursor = cursor, text = text)
    
    def mouse_down(self, game, pos):
        if game.variables["Charger_Plugged"] == False:
            if game.hotbar.selected == "Laptop Charger" and game.items["Laptop Charger"].collected:
                game.hotbar.remove_item("Laptop Charger")
                game.variables["Charger_Plugged"] = True
                game.scenes["Front_Room"].overlays["Wire"].enabled = True
                game.scenes["Right_Room"].overlays["Wire"].enabled = True
                game.scenes["Desk"].overlays["Wire"].enabled = True
                game.tipbar.force_text("Plugged the charger into the laptop.")
            else:
                game.tipbar.force_text("You can't seem to turn the laptop on.")
        else:
            super().mouse_down(game, pos)

class Safe_Transition(Transition):
    def __init__(self, x, y, x2, y2, *, scene: str, cursor="Front", text=""):
        super().__init__(x, y, x2, y2, scene = scene, cursor = cursor, text = text)
    
    def mouse_down(self, game, pos):
        if game.variables["Safe_Locked"] == True:
            game.tipbar.force_text("The safe is locked.")
        else:
            super().mouse_down(game, pos)
            game.tipbar.force_text("")

#

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
    
    def update(self, game, delta=0):
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

class GoldKey_Interaction(Item_Interaction):
    def __init__(self, x, y, x2, y2, *, cursor="Front", text=""):
        super().__init__(x, y, x2, y2, cursor=cursor, text=text)

    def mouse_down(self, game, pos):
        if game.hotbar.selected == "Broom" and game.items["Broom"].collected:
            game.hotbar.remove_item("Broom")
            confirm = super().mouse_down(game, pos)
            if confirm == True:
                game.scenes["Vent_Removed"].overlays["GoldKey"].enabled = False
        elif game.hotbar.selected == "Hammer":
            game.tipbar.force_text("Even with a trusty hammer were you still unable to reach the key. It's a lot farther down there than expected.")
        elif game.hotbar.selected != None:
            game.tipbar.force_text("Doesn't seem to help get the key.")
        else:
            game.tipbar.force_text("Key is too far to reach! There should be something long enough to get it from this distance.")

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

class Wall_Interaction(Item_Interaction):
    def __init__(self, x, y, x2, y2, *, cursor="Front", text=""):
        super().__init__(x, y, x2, y2, cursor=cursor, text=text)
        self.item = "Phillips Screwdriver"

    def give_item(self, game, pos):
        item = game.items[self.item]
        if item.collected:
            return False
        if game.hotbar.add_item(item):
            item.collected = True
            self.visible = False
            self.enabled = False
            game.hover(pos)
            game.tipbar.force_text("Acquired " + item.name + ".")
            return True
    
    def mouse_down(self, game, pos):
        if game.hotbar.selected == "Hammer" and game.items["Hammer"].collected:
            confirm = self.give_item(game, pos)
            if confirm == True:
                game.scenes["Poster_Removed"].change_bg(pygame.image.load('Images/Scenes/Poster/BrokenWall.png'))

class Paper_Interaction(Item_Interaction):
    def __init__(self, x, y, x2, y2, *, cursor="Front", text=""):
        super().__init__(x, y, x2, y2, cursor=cursor, text=text)

    def mouse_down(self, game, pos):
        confirm = super().mouse_down(game, pos)
        if confirm == True:
            game.scenes["Safe_Opened"].overlays["Paper"].enabled = False

#

class Screw(Interaction):
    def __init__(self, x, y, type):
        gap = 10
        size = 15
        super().__init__(x-gap, y-gap, size+(gap*2), size+(gap*2))

        self.type = type
        image = type == "Phillips" and pygame.image.load('Images/Others/phillipsScrew.png') or pygame.image.load('Images/Others/flatheadScrew.png')
        self.image = pygame.transform.scale(image, (int(size), int(size)))
        self.center = (x+7, y+7)
        self.angle = 0 # in degrees
        self.cursor = "Hand"
        self.requires_tool = True
        self.visible = True
        self.tick = -1

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=self.center)
        #pygame.draw.rect(screen, (255,0,0), self.rect) DEBUG
        screen.blit(rotated_image, rect)

    def update(self, game, delta=0):
        if self.tick < 0:
            return
        self.tick += delta
        if self.tick < 1.5:
            self.angle = 360 * self.tick
        else:
            self.tick = -1
            self.angle = 0
            image = pygame.image.load('Images/Others/screwHole.png')
            self.image = pygame.transform.scale(image, (15,15))

            if self.type == "Flathead":
                game.variables["Vent_Screws"] -= 1
            elif self.type == "Phillips":
                game.variables["Powerbox_Screws"] -= 1
            game.variables["Debounce"] -= 1
            self.updateOnTick = False
    
    def mouse_down(self, game, pos):
        required = self.type + " Screwdriver"
        if game.hotbar.selected == required and game.items[required].collected:
            self.tick = 0
            self.updateOnTick = True
            game.tipbar.force_text("Unscrewed the screw.")
            game.variables["Debounce"] += 1
            self.enabled = False
            game.hover(pos)
        elif (required == "Flathead Screwdriver" and game.hotbar.selected == "Phillips Screwdriver") or (required == "Phillips Screwdriver" and game.hotbar.selected == "Flathead Screwdriver"):
            game.tipbar.force_text("This screwdriver doesn't seem to fit. You'll need a different one for it.")
        else:
            game.tipbar.force_text("This doesn't seem to fit.")

class Vent_Interaction(Transition):
    def __init__(self, x, y, x2, y2, *, scene: str, cursor="Front", text=""):
        super().__init__(x, y, x2, y2, scene = scene, cursor = cursor, text = text)
    
    def mouse_down(self, game, pos):
        if game.variables["Vent_Screws"] > 0:
            if game.variables["Debounce"] > 0:
                return
            game.tipbar.force_text("This vent won't budge.")
        else:
            super().mouse_down(game, pos)

class Power_Interaction(Transition):
    def __init__(self, x, y, x2, y2, *, scene: str, cursor="Front", text=""):
        super().__init__(x, y, x2, y2, scene = scene, cursor = cursor, text = text)
        self.first_time = False
    
    def mouse_down(self, game, pos):
        if game.variables["Powerbox_Screws"] > 0:
            if game.variables["Debounce"] > 0:
                return
            game.tipbar.force_text("This powerbox won't open.")
        else:
            super().mouse_down(game, pos)
            if self.first_time == False:
                self.first_time = True
                game.tipbar.force_text("What a mess..")

class Safe_Button(Image_Interaction):
    def __init__(self, x, y, image, scale, *, input, clicked_image):
        super().__init__(x, y, image, scale)
        self.cursor = "Hand"
        self.initial_image = image
        self.clicked_image = clicked_image
        self.input = input
    
    def mouse_down(self, game, pos):
        self.new_image(game.screen, image = self.clicked_image)
        if game.variables["Safe_Locked"]:
            if self.input == "C":
                game.variables["Safe_Code"] = ""
            elif self.input == "#":
                game.scene.interactions[0].confirm(game)
            elif len(game.variables["Safe_Code"]) < 4:
                game.variables["Safe_Code"] += str(self.input)

    def mouse_up(self, game, pos):
        self.new_image(game.screen, image = self.initial_image)

class Safe_Code(Interaction):
    def __init__(self, x, y, x2, y2):
        super().__init__(x, y, x2, y2)
        pygame.font.init()
        #print(pygame.font.get_fonts())
        self.enabled = False
        self.tick = -1
        self.updateOnTick = True
        self.placeholderText = ""

    def update(self, game, delta=0):
        if game.variables["Safe_Code"] != "":
            self.placeholderText = ""
        font = pygame.font.SysFont('arial', 35, bold=True) # workaround; cannot be pickled
        color = (190, 237, 47)
        if self.tick >= 0 and self.tick % 0.1 < 0.05:
            color = (255, 255, 255)
            
        text = font.render(game.variables["Safe_Code"] == "" and self.placeholderText or game.variables["Safe_Code"], True, color)
        game.screen.blit(text, (self.rect.x, self.rect.y))

        if self.tick >= 0:
            self.tick += delta
            if self.tick > 0.5:
                self.tick = -1
                game.variables["Debounce"] -= 1

    def confirm(self, game):
        if game.variables["Debounce"] > 0 or game.variables["Safe_Code"] == "":
            return
        elif game.variables["Safe_Code"] == game.variables["Correct_Code1"]:
            game.variables["Safe_Code"] = ""
            self.placeholderText = "=)"
            self.tick = 0
            game.variables["Debounce"] += 1
            game.variables["Safe_Locked"] = False
            game.tipbar.force_text("A click has been made.")
        else:
            game.variables["Safe_Code"] = ""
            self.placeholderText = ">:("
            self.tick = 0
            game.variables["Debounce"] += 1
            game.tipbar.force_text('"INCORRECT"')

class Laptop_Textbox(Interaction):
    def __init__(self, x, y, x2, y2):
        super().__init__(x, y, x2, y2)
        pygame.font.init()
        self.updateOnTick = True
        self.tick = 0
        self.cursor = "Hand"
        self.hold_tick = 0
        self.backspace_tick = 0
    
    def update(self, game, delta=0):
        if game.variables["Laptop_Typing"] == True:
            self.tick += delta
            if self.tick >= 1:
                self.tick -= 1
            
            if game.variables["Backspace"] == True: # just to make holding backspace a thing (not gonna program holding other keys)
                self.hold_tick += delta
                if self.hold_tick > 0.5:
                    self.backspace_tick += delta
                    if self.backspace_tick > 0.05:
                        self.backspace_tick -= 0.05
                        game.variables["Laptop_Prompt"] = game.variables["Laptop_Prompt"][:-1]
            else:
                self.hold_tick = 0
                self.backspace_tick = 0
        else:
            self.tick = 0
        text = game.variables["Laptop_Prompt"] + ((self.tick < 0.5 and game.variables["Laptop_Typing"]) and "_" or "")
        font = pygame.font.SysFont('arial', 22) # workaround; cannot be pickled
        color = (255, 255, 255)

        rendered_text = font.render(text, True, color)
        game.screen.blit(rendered_text, (self.rect.x, self.rect.y))

    def mouse_down(self, game, pos):
        game.variables["Laptop_Typing"] = True
        return "Typing"

    def confirm(self, game):
        if not game.variables["Door_Lock"]:
            return
        
        if game.variables["Laptop_Prompt"] == game.variables["Correct_Code2"]:
            game.scenes["Laptop"].change_bg(pygame.image.load('Images/Scenes/Laptop/Unlocked.png'))
            game.scenes["Laptop"].overlays["OnSwitch"].enabled = True
            game.scenes["Laptop"].overlays["Incorrect"].enabled = False
            game.scenes["Laptop"].interactions[1].enabled = True
            self.updateOnTick = False
            self.enabled = False
        else:
            game.scenes["Laptop"].overlays["Incorrect"].enabled = True
        game.variables["Laptop_Prompt"] = ""

class Laptop_Switch(Interaction):
    def __init__(self, x, y, x2, y2):
        super().__init__(x, y, x2, y2)
        self.enabled = False
        self.cursor = "Hand"
        self.text = '"Door Lock"'
        self.first_time = False

    def mouse_down(self, game, pos):
        game.variables["Door_Lock"] = not game.variables["Door_Lock"]

        game.scenes["Laptop"].overlays["OffSwitch"].enabled = not game.variables["Door_Lock"]
        game.scenes["Laptop"].overlays["OnSwitch"].enabled = game.variables["Door_Lock"]

        if self.first_time == False:
            self.first_time = True
            game.tipbar.force_text("Must of did something.")

class Wires(Interaction):
    def __init__(self, x, y, x2, y2):
        super().__init__(x, y, x2, y2)
        self.cursor = "Hand"
        self.text = "Broken Wires"

    def mouse_down(self, game, pos):
        if game.hotbar.selected == "Electric Tape" and game.items["Electric Tape"].collected:
            game.hotbar.remove_item("Electric Tape")
            self.enabled = False
            game.scenes["Power_Opened"].overlays["Broken_Wires"].enabled = False
            game.scenes["Power_Opened"].overlays["Fixed_Wires"].enabled = True
            game.variables["Powerbox_Fixed"] = True

            self.text = "Fixed Wires"
            game.tipbar.force_text("Fixed.")
            game.hover(pos)

class Door(Interaction):
    def __init__(self, x, y, x2, y2):
        super().__init__(x, y, x2, y2)
        self.cursor = "Hand"
        self.text = "The Door"

    def mouse_down(self, game, pos):
        pass
