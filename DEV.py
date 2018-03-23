import pygame
from pygame.locals import *
import sys
import math
import settings
from functions import *


class screen:
    def __init__(self, Window, Canvas, Shell):
        self.Window = Window
        self.surface = pygame.Surface(settings.WindowSize)

        self.setTexts()

        self.Turtle = Turtle
        self.Canvas = Canvas
        self.Shell = Shell

    def blitAll(self):

        self.surface.blit(self.Canvas.surface, (0, 0))
        self.surface.blit(self.Shell.surface, settings.ShellPosition)
        self.blitTurtle()
        self.surface.blit(self.textSurface, settings.textPosition)

        self.Window.blit(self.surface, (0, 0))

    def blitTurtle(self):
        if not self.Turtle.isShow:
            return
        Turtle = self.Turtle
        TPo = [Turtle.position[0] - (Turtle.turtleSize) + self.Canvas.relative[0],
               Turtle.position[1] - (Turtle.turtleSize) + self.Canvas.relative[1]]

        self.surface.blit(Turtle.surface, TPo)

    def setTexts(self):
        texts = settings.texts

        self.textSurface = pygame.Surface(settings.textSize)
        self.textSurface.fill(settings.textBackground)

        for i, t in enumerate(texts):
            texteSurface = settings.fontObj.render(t, True, settings.textColor)
            texteRect = texteSurface.get_rect()
            texteRect.topleft = (0, 5 + i * 30)

            self.textSurface.blit(texteSurface, texteRect)


class turtle:  # 画笔
    def __init__(self):
        self.reset()
        self.drawTurtle()

    def reset(self):
        self.isShow = True
        self.position = [0, 0]
        self.angle = 0
        self.radian = 0
        self.color = [0, 0, 0]

    def drawTurtle(self):
        turtleSize = settings.TurtleSize
        self.turtleSize = turtleSize

        position1 = (turtleSize + math.sin(self.radian) * turtleSize,
                     turtleSize - math.cos(self.radian) * turtleSize)
        position2 = (turtleSize + math.sin(self.radian + ((math.pi / 3) * 2)) * turtleSize,
                     turtleSize - math.cos(self.radian + ((math.pi / 3) * 2)) * turtleSize)
        position3 = (turtleSize + math.sin(self.radian + ((math.pi / 3) * 4)) * turtleSize,
                     turtleSize - math.cos(self.radian + ((math.pi / 3) * 4)) * turtleSize)

        Surface = pygame.Surface((turtleSize * 2, turtleSize * 2),
                                 flags=SRCALPHA)
        pygame.draw.line(Surface, self.color, position1, position2)
        pygame.draw.line(Surface, self.color, position2, position3)
        pygame.draw.line(Surface, self.color, position3, position1)

        self.surface = Surface

    def move(self, lenth, isForward):

        if isForward:
            self.position[0] += int(math.sin(self.radian) * lenth)
            self.position[1] -= int(math.cos(self.radian) * lenth)
        else:
            self.position[0] -= int(math.sin(self.radian) * lenth)
            self.position[1] += int(math.cos(self.radian) * lenth)

        return self.position

    def rotate(self, angle, isClockwise):

        if isClockwise:
            self.angle += angle
        else:
            self.angle -= angle
        self.angle -= 360 if self.angle >= 360 else 0
        self.radian = AngleToRadian(self.angle)

        self.drawTurtle()


class shell:
    def __init__(self):
        self.surface = pygame.Surface(settings.ShellSize)
        self.surface.fill(settings.shellColor)

        self.reset()

        self.blitText()

    def getStr(self):
        Str = input().upper()
        Arr = Str.split(" ")
        return self.PhraseAnalyse(Arr, 0, len(Arr) - 1)

    def reset(self):
        self.Str = ""
        self.history = []

    def PhraseAnalyse(self, Arr, start, end, delay=True):
        if len(Arr) == 0:
            return
        if start > end:
            return
        Crr = start
        nbr = 0
        while Crr <= end:
            STR = Arr[Crr]
            if STR == "AV" or STR == "TD" or STR == "RE" or STR == "TG":
                nbr = int(Arr[Crr + 1])
                self.splitActions(STR, nbr, delay)
                Crr += 2
            elif STR == "FCC":
                color = Arr[Crr + 1]
                Canvas.actions.append([STR, color])

                Crr += 2
            elif STR == "REPETE":
                nbr = int(Arr[Crr + 1])
                sphereStart = Crr + 2
                sphereEnd = CutSphere(Arr, sphereStart, end)
                for i in range(nbr):
                    self.PhraseAnalyse(Arr, sphereStart + 1, sphereEnd - 1,
                                       delay)
                Crr = sphereEnd + 1
            elif STR == "VE" or STR == "BC" or STR == "LC" or\
                    STR == "CT" or STR == "MT":
                Canvas.actions.append([STR, 0])

                Crr += 1
            elif STR == "EXIT":
                return True
            elif STR == "ROLLBACK":
                self.rollBack()

                return
            else:
                Crr += 1
        return False

    def splitActions(self, STR, DATA, delay):
        if delay:
            for i in range(10):
                length = DATA / (10.0 - i)
                DATA -= length
                Canvas.actions.append([STR, length])
        else:
            Canvas.actions.append([STR, DATA])

    def rollBack(self):
        self.history = self.history[0:-1]

        Canvas.canvasReset()
        Turtle.reset()

        for i in self.history:
            self.PhraseAnalyse(i, 0, len(i) - 1, False)

        self.blitText()

    def Input(self, char):
        self.Str += str(char)

        self.blitText()

    def Delete(self):
        self.Str = self.Str[0:-1]

        self.blitText()

    def Exec(self):
        Arr = self.Str.split(" ")

        self.PhraseAnalyse(Arr, 0, len(Arr) - 1)

        if self.checkHistory(Arr):
            self.history.append(Arr)

        self.Str = ""

        self.blitText()

    def checkHistory(self, Arr):
        for i in Arr:
            if i == "ROLLBACK" or i == "EXIT":
                return False
        return True

    def blitText(self):
        texts = []
        texts.append(self.Str)
        if len(self.history) != 0:
            texts.append(self.history[-1])
        if len(self.history) >= 2:
            texts.append(self.history[-2])
        if len(self.history) >= 3:
            texts.append(self.history[-3])

        self.surface.fill(settings.shellColor)

        for i, t in enumerate(texts):

            print(t)

            message = ""
            for j in t:
                message += ("" + j + (" " if type(t) == list else ""))

            texteSurface = settings.fontObj.render("?" + message + "_", True,
                                                   settings.textColor)
            texteRect = texteSurface.get_rect()
            texteRect.topleft = (5, 70 - i * 20)

            self.surface.blit(texteSurface, texteRect)


class canvas:
    def __init__(self, Turtle):
        self.canvasReset()

        self.actions = []

        self.Turtle = Turtle

        self.relative = settings.CanvasRelativePosition

    def canvasReset(self):
        self.surfaceReset()
        self.isPenDown = True

    def surfaceReset(self):
        self.surface = pygame.Surface(settings.CanvasSize)
        self.surface.fill((230, 230, 230))

    def drawLine(self, start, end):
        pygame.draw.line(self.surface, self.Turtle.color,
                         RelativeToAbsolute(start),
                         RelativeToAbsolute(end))

    def action(self):
        if len(self.actions) == 0:
            return
        actionName, actionData = self.actions.pop(0)
        if actionName == "AV" or actionName == "RE":
            Start = [self.Turtle.position[0], self.Turtle.position[1]]
            self.Turtle.move(actionData, actionName == "AV")
            End = self.Turtle.position

            if self.isPenDown:
                self.drawLine(Start, End)

        elif actionName == "TD" or actionName == "TG":
            self.Turtle.rotate(actionData, actionName == "TD")

        elif actionName == "FCC" and len(actionData) == 6:
            self.Turtle.color = [int(actionData[0:2], 16),
                                 int(actionData[2:4], 16),
                                 int(actionData[4:6], 16)]

            self.Turtle.drawTurtle()

        elif actionName == "LC" or actionName == "BC":
            self.isPenDown = actionName == "BC"

        elif actionName == "CT" or actionName == "MT":
            self.Turtle.isShow = actionName == "MT"

        elif actionName == "VE":
            Shell.reset()
            self.canvasReset()
            self.Turtle.reset()


def init():
    pygame.init()

    Window = pygame.display.set_mode(settings.WindowSize)
    pygame.display.set_caption(settings.CaptionBanner)
    pygame.key.set_repeat(200, 50)
    fpsClock = pygame.time.Clock()

    return Window, fpsClock


Window, fpsClock = init()

Turtle = turtle()
Canvas = canvas(Turtle)
Shell = shell()
Screen = screen(Window, Canvas, Shell)

exit = False

count = 0
while not exit:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit = True
            break
        KeyboardManager(event, Shell)

    Canvas.action()
    Screen.blitAll()
    pygame.display.update()
    fpsClock.tick(10)
pygame.quit()
sys.exit()
