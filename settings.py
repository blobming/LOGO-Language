import pygame

WindowSize = (700, 600)
CanvasSize = (500, 500)
ShellSize = (500, 100)
textSize = (200, 600)
textBackground = (200, 200, 200)

ShellPosition = (0, 500)
textPosition = (500, 0)

CaptionBanner = "LOGO Canvas"
TurtleSize = 5
CanvasRelativePosition = (250, 250)

pygame.font.init()
fontObj = pygame.font.Font('freesansbold.ttf', 15)

textColor = (255, 255, 255)
shellColor = (0, 0, 0)

texts = ["  All Commands:",
         "AV pixels",
         "RE pixels",
         "TD degrees",
         "TG pixels",
         "FCC color",
         "LC(pen up)",
         "BC(pen down)",
         "VE(clear)",
         "CT(hide pen)",
         "MT(show pen)",
         "REPETE times [commands]"]
