import pygame

class Button:
    def __init__(self, color, x, y, width, height, text='', action = None):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen, font, outline=None):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        
        if self.text != '':
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
screen = pygame.display.set_mode((1000, 700))

class Image_Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.is_clicked == False:
                self.clicked = True
                action = True
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
