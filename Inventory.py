import pygame

class Item:
    def __init__(self, x, y, image):
        self.image = image
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
        else:
            pygame.draw.rect(screen, (120,120,120), self.rect, 2)

        if self.item:
            padding = 4
            scaled_item = pygame.transform.scale(
                self.item.image,
                (self.rect.width - 2*padding, self.rect.height - 2*padding)
            )
            screen.blit(scaled_item, (self.rect.x + padding, self.rect.y + padding))

class Hotbar:
    def __init__(self, x, y, slot_size, num_slots, slot_img=None):
        self.slots = []
        for i in range(num_slots):
            slot_x = x + i * (slot_size + 10)
            self.slots.append(InventorySlot(slot_x, y, slot_size, slot_img))

    def draw(self, screen):
        for slot in self.slots:
            slot.draw(screen)