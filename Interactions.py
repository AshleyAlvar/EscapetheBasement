import pygame

# base classes

class Interaction:
    def __init__(self, x, y, x2, y2):
        self.type = "Default"
        self.rect = pygame.Rect(x, y, x2, y2) # rectangle will not show in the game; only used as to detect clicks

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
class Image_Interaction:
    def __init__(self, x, y, image, scale):
        self.type = "Default"
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.scale = scale
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
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

# derived classes

class Transition(Interaction):
    def __init__(self, x, y, x2, y2, *, scene):
        super().__init__(x, y, x2, y2)
        self.type = "Transition"
        self.scene = scene # scene name (string)