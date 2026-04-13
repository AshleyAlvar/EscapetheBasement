import pygame

class Item:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.scale = scale
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False

    def draw(self, screen):
        if not self.collected:
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
            padding = 4
            scaled_item = pygame.transform.scale(
                self.item.image,
                (self.rect.width - 4*padding, self.rect.height - 4*padding)
            )
            screen.blit(scaled_item, (self.rect.x + padding, self.rect.y + padding))

class Hotbar:
    def __init__(self, x, y, slot_size, num_slots, slot_img=None):
        self.slots = []
        for i in range(num_slots):
            slot_x = x + i * (slot_size + 10)
            self.slots.append(InventorySlot(slot_x, y, slot_size, slot_img))

        self.selected_index = None
    
    def handle_click(self, mouse_pos):
        for i, slot in enumerate(self.slots):
            if slot.rect.collidepoint(mouse_pos):
                self.selected_index = i if self.selected_index != i else None
    
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
    