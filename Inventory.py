import pygame

class Item:
    def __init__(self, x, y, image, scale, *, name, bg_image=None):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.scale = scale
        self.rect = self.image.get_rect(topleft=(x, y))
        self.name = name
        
        self.collected = False
        self.visible = False

        if bg_image != None:
            width = bg_image.get_width()
            height = bg_image.get_height()
            self.bg_image = pygame.transform.scale(bg_image, (int(width), int(height)))
            self.bg_rect = self.bg_image.get_rect(topleft=(x, y))
        else:
            self.bg_image = None

    def draw(self, screen):
        if not self.collected and self.visible:
            if self.bg_image != None:
                screen.blit(self.bg_image, self.bg_rect)
            else:
                screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class InventorySlot:
    def __init__(self, x, y, size, slot_img=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.item = None
        self.slot_img = slot_img

    def draw(self, screen):
        if self.slot_img:
            scaled_slot = pygame.transform.scale(self.slot_img, (self.rect.width, self.rect.height))
            screen.blit(scaled_slot, self.rect.topleft)

        if self.item:
            """
            scaled_item = pygame.transform.scale(
                self.item.image,
                (self.rect.width, self.rect.height)
            )
            """
            screen.blit(self.item.image, (self.rect.x, self.rect.y))

class Hotbar:
    def __init__(self, x, y, slot_size, num_slots, slot_img=None):
        self.slots = []
        for i in range(num_slots):
            slot_x = x + i * (slot_size + 10)
            self.slots.append(InventorySlot(slot_x, y, slot_size, slot_img))

        self.selected_index = None
        self.selected = ""
    
    def handle_click(self, mouse_pos):
        for i, slot in enumerate(self.slots):
            if slot.rect.collidepoint(mouse_pos) and slot.item is not None:
                self.selected_index = i if self.selected_index != i else None
                self.selected = slot.item.name if self.selected != slot.item.name else None
                return True
        return False
    
    def get_selected_item(self):
        if self.selected_index is not None:
            return self.slots[self.selected_index].item
        return None

    def draw(self, screen):
        for i, slot in enumerate(self.slots):
            slot.draw(screen)
            if i == self.selected_index and slot.item is not None:
                pygame.draw.rect(screen, (255, 255, 0), slot.rect, 3)

    def add_item(self, item):  
        for slot in self.slots:
            if slot.item is None:
                slot.item = item
                return True
        return False

    def remove_item(self, name): # simply delinks the item rather than delete them; all items are just pre-defined beforehand
        for slot in self.slots:
            if slot.item is not None:
                if slot.item.name == name:
                    if self.selected == slot.item.name:
                        self.selected_index = None
                        self.selected = None
                    slot.item = None
                    break
    