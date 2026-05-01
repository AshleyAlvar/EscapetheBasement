import pygame
import Interactions

class Scene:
    def __init__(self, /,*, background, interactions=[], items=[], overlays=[]):
        self.background = background
        self.interactions = interactions
        self.items = items
        self.overlays = overlays

    def change_bg(self, background):
        self.background = background

Scenes = {
    # PRIMARY
    "Front_Room" : Scene(
        background = pygame.image.load('Images/Scenes/Main1/Scene.png'),
        interactions = [
            Interactions.Transition(0,0,100,825, # LEFT
                scene = "Left_Room",
            ),
            Interactions.Transition(1466-100,0,100,825, # RIGHT
                scene = "Right_Room",
            ),
        ],
    ),
    "Right_Room" : Scene(
        background = pygame.image.load('Images/Scenes/Main2/Scene.png'),
        interactions = [
            Interactions.Transition(0,0,100,825, # LEFT
                scene = "Front_Room",
            ),
            Interactions.Transition(1466-100,0,100,825, # RIGHT
                scene = "Back_Room",
            ),
        ],
    ),
    "Back_Room" : Scene(
        background = pygame.image.load('Images/Scenes/Main3/Scene.png'),
        interactions = [
            Interactions.Transition(0,0,100,825, # LEFT
                scene = "Right_Room",
            ),
            Interactions.Transition(1466-100,0,100,825, # RIGHT
                scene = "Left_Room",
            ),
        ],
    ),
    "Left_Room" : Scene(
        background = pygame.image.load('Images/Scenes/Main4/Scene.png'),
        interactions = [
            Interactions.Transition(0,0,100,825, # LEFT
                scene = "Back_Room",
            ),
            Interactions.Transition(1466-100,0,100,825, # RIGHT
                scene = "Front_Room",
            ),
        ],
    ),
    # SECONDARY
    "Front_Cabinet" : Scene(
        background = pygame.image.load('Images/Scenes/Cabinet/Scene.png'),
    ),
    "Behind_Cabinet" : Scene(
        background = pygame.image.load('Images/Scenes/Cabinet/BehindCabinet.png'),
    ),
    "Desk" : Scene(
        background = pygame.image.load('Images/Scenes/Desk/Scene.png'),
    ),
    "Safe" : Scene(
        background = pygame.image.load('Images/Scenes/Safe/Scene.png'),
    ),
    "Power" : Scene(
        background = pygame.image.load('Images/Scenes/Power/Scene.png'),
    ),
    "Poster" : Scene(
        background = pygame.image.load('Images/Scenes/Poster/Scene.png'),
    ),
    "Vent" : Scene(
        background = pygame.image.load('Images/Scenes/Vent/Scene.png'),
    ),
    # ---
    "Calendar" : Scene(
        background = pygame.image.load('Images/Scenes/CalendarScene.png'),
    ),
    "Clock" : Scene(
        background = pygame.image.load('Images/Scenes/ClockScene.png'),
    ),
    "Laptop" : Scene(
        background = pygame.image.load('Images/Scenes/LaptopScene.png'),
    ),
    "TrashBin" : Scene(
        background = pygame.image.load('Images/Scenes/TrashBinScene.png'),
    ),
}