import pygame
import Interactions

class Scene:
    def __init__(self, /,*, background, interactions=[], items=[], overlays=[], name=""):
        self.background = background
        self.interactions = interactions
        self.items = items
        self.overlays = overlays
        self.name = name # only reserved for main 1 to 4

    def change_bg(self, background):
        self.background = background

Scenes = {
    # PRIMARY
    "Front_Room" : Scene(
        background = pygame.image.load('Images/Scenes/Main1/Scene.png'),
        name = "Front_Room",
        interactions = [
            Interactions.Transition(49,618,75,75,
                scene = "Behind_Cabinet",
                cursor = "Back",
            ),
            Interactions.Transition(43,404,334,262,
                scene = "Front_Cabinet",
            ),
            Interactions.Transition(831,378,237,148,
                scene = "Desk",
            ),
            Interactions.Transition(668,358,80,56,
                scene = "Power",
            ),
            Interactions.Transition(877,295,57,57,
                scene = "Clock",
            ),
            Interactions.Transition(791,445,39,64,
                scene = "TrashBin",
            ),

            Interactions.Transition(0,0,100,825, # LEFT
                scene = "Left_Room",
                cursor = "Left",
            ),
            Interactions.Transition(1466-100,0,100,825, # RIGHT
                scene = "Right_Room",
                cursor = "Right",
            ),
        ],
    ),
    "Right_Room" : Scene(
        background = pygame.image.load('Images/Scenes/Main2/Scene.png'),
        name = "Right_Room",
        interactions = [
            Interactions.Transition(167,517,128,129,
                scene = "TrashBin",
                cursor = "Back",
            ),
            Interactions.Transition(221,387,297,225,
                scene = "Desk",
            ),
            Interactions.Transition(246,259,70,86,
                scene = "Clock",
            ),
            Interactions.Transition(827,256,158,203,
                scene = "Poster",
            ),
            Interactions.Transition(727,307,82,50,
                scene = "Calendar",
            ),

            Interactions.Transition(0,0,100,825, # LEFT
                scene = "Front_Room",
                cursor = "Left",
            ),
            Interactions.Transition(1466-100,0,100,825, # RIGHT
                scene = "Back_Room",
                cursor = "Right",
            ),
        ],
    ),
    "Back_Room" : Scene(
        background = pygame.image.load('Images/Scenes/Main3/Scene.png'),
        name = "Back_Room",
        interactions = [
            Interactions.Transition(244,213,214,362,
                scene = "Poster",
            ),
            Interactions.Transition(100,264,130,90,
                scene = "Calendar",
            ),
            Interactions.Transition(799,441,82,77,
                scene = "Safe",
            ),
            Interactions.Transition(1085,382,318,279,
                scene = "Front_Cabinet",
            ),

            Interactions.Transition(0,0,100,825, # LEFT
                scene = "Right_Room",
                cursor = "Left",
            ),
            Interactions.Transition(1466-100,0,100,825, # RIGHT
                scene = "Left_Room",
                cursor = "Right",
            ),
        ],
    ),
    "Left_Room" : Scene(
        background = pygame.image.load('Images/Scenes/Main4/Scene.png'),
        name = "Left_Room",
        interactions = [
            Interactions.Transition(667,377,101,144,
                scene = "Front_Cabinet",
            ),
            Interactions.Transition(273,468,139,103,
                scene = "Safe",
            ),
            Interactions.Transition(1188,355,153,109,
                scene = "Power",
            ),

            Interactions.Transition(0,0,100,825, # LEFT
                scene = "Back_Room",
                cursor = "Left",
            ),
            Interactions.Transition(1466-100,0,100,825, # RIGHT
                scene = "Front_Room",
                cursor = "Right",
            ),
        ],
    ),
    # SECONDARY
    "Front_Cabinet" : Scene(
        background = pygame.image.load('Images/Scenes/Cabinet/Scene.png'),
        interactions = [
            Interactions.Transition(0,625,1466,200,
                scene = "Previous",
                cursor = "Back",
            ),
        ],
    ),
    "Behind_Cabinet" : Scene(
        background = pygame.image.load('Images/Scenes/Cabinet/BehindCabinet.png'),
        interactions = [
            Interactions.Transition(0,575,1466,250,
                scene = "Previous",
                cursor = "Back",
            ),
        ],
    ),
    "Desk" : Scene(
        background = pygame.image.load('Images/Scenes/Desk/Scene.png'),
        interactions = [
            Interactions.Transition(220,382,213,262,
                scene = "TrashBin",
            ),
            Interactions.Transition(677,108,226,173,
                scene = "Laptop",
            ),
            
            Interactions.Transition(0,725,1466,100,
                scene = "Previous",
                cursor = "Back",
            ),
        ],
    ),
    "Safe" : Scene(
        background = pygame.image.load('Images/Scenes/Safe/Scene.png'),
        interactions = [
            Interactions.Transition(0,725,1466,100,
                scene = "Previous",
                cursor = "Back",
            ),
            Interactions.Transition(0,0,1466,100,
                scene = "Previous",
            ),
            Interactions.Transition(0,0,200,825,
                scene = "Previous",
                cursor = "Left",
            ),
            Interactions.Transition(1266,0,200,825,
                scene = "Previous",
                cursor = "Right",
            ),
        ],
    ),
    "Power" : Scene(
        background = pygame.image.load('Images/Scenes/Power/Scene.png'),
        interactions = [
            Interactions.Transition(0,625,1466,200,
                scene = "Previous",
                cursor = "Back",
            ),
        ],
    ),
    "Poster" : Scene(
        background = pygame.image.load('Images/Scenes/Poster/Scene.png'),
        interactions = [
            Interactions.Transition(210,285,246,159,
                scene = "Calendar",
            ),
            Interactions.Transition(0,725,1466,100,
                scene = "Previous",
                cursor = "Back",
            ),
        ],
    ),
    "Vent" : Scene(
        background = pygame.image.load('Images/Scenes/Vent/Scene.png'),
        interactions = [
            Interactions.Transition(0,650,1466,175,
                scene = "Previous",
                cursor = "Back",
            ),
            Interactions.Transition(0,0,200,825,
                scene = "Previous",
                cursor = "Left",
            ),
            Interactions.Transition(1266,0,200,825,
                scene = "Previous",
                cursor = "Right",
            ),
        ],
    ),
    # ---
    "Calendar" : Scene(
        background = pygame.image.load('Images/Scenes/CalendarScene.png'),
        interactions = [
            Interactions.Transition(0,700,1466,125,
                scene = "Previous",
                cursor = "Back",
            ),
            Interactions.Transition(0,0,200,825,
                scene = "Previous",
                cursor = "Left",
            ),
            Interactions.Transition(1266,0,200,825,
                scene = "Previous",
                cursor = "Right",
            ),
        ],
    ),
    "Clock" : Scene(
        background = pygame.image.load('Images/Scenes/ClockScene.png'),
        interactions = [
            Interactions.Transition(0,700,1466,125,
                scene = "Previous",
                cursor = "Back",
            ),
            Interactions.Transition(0,0,400,825,
                scene = "Previous",
                cursor = "Left",
            ),
            Interactions.Transition(1066,0,400,825,
                scene = "Previous",
                cursor = "Right",
            ),
        ],
    ),
    "Laptop" : Scene(
        background = pygame.image.load('Images/Scenes/LaptopScene.png'),
        interactions = [
            Interactions.Transition(0,750,1466,75,
                scene = "Previous",
                cursor = "Back",
            ),
            Interactions.Transition(0,0,200,825,
                scene = "Previous",
                cursor = "Left",
            ),
            Interactions.Transition(1266,0,200,825,
                scene = "Previous",
                cursor = "Right",
            ),
        ],
    ),
    "TrashBin" : Scene(
        background = pygame.image.load('Images/Scenes/TrashBinScene.png'),
        interactions = [
            Interactions.Transition(0,0,1466,100,
                scene = "Previous",
                cursor = "Back",
            ),
            Interactions.Transition(0,750,1466,75,
                scene = "Previous",
            ),
            Interactions.Transition(0,0,400,825,
                scene = "Previous",
                cursor = "Left",
            ),
            Interactions.Transition(1066,0,400,825,
                scene = "Previous",
                cursor = "Right",
            ),
        ],
    ),
}