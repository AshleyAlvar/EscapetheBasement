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
    
screen = pygame.display.set_mode((1280, 720))
var = "test"

class Image_Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.scale = scale
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
    
    def new_image(self, image):
        width = image.get_width()
        height = image.get_height()
        scale = self.scale
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Volume:
    def __init__(self, x, y, barImage, sliderImage, min_val=0.0, max_val=1.0, start_val=1.0):

        self.track_img = barImage
        self.knob_img = sliderImage

        self.x = x
        self.y = y

        self.barImage = self.barImage.get_rect(topleft=(x, y))

        self.slider_rect = self.sliderImage.get_rect()
        self.slider_rect.centery = self.bar_rect.centery

        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val

        self.dragging = False

        self.update_knob_position()

    def draw(self, screen):
        screen.blit(self.barImage, self.bar_rect)

        screen.blit(self.sliderImage, self.slider_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.slider_rect.collidepoint(event.pos):
                    self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value(event.pos[0])

    def update_value(self, mouse_x):
        relative_x = mouse_x - self.bar_rect.x
        relative_x = max(0, min(self.bar_rect.width, relative_x))

        self.value = self.min_val + (relative_x / self.bar_rect.width) * (self.max_val - self.min_val)

        self.update_knob_position()

        pygame.mixer.music.set_volume(self.value)

    def update_knob_position(self):
        percent = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.knob_rect.centerx = self.track_rect.x + int(percent * self.track_rect.width)
        self.knob_rect.centery = self.track_rect.centery
