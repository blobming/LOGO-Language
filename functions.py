from pygame.locals import *
import settings
import math


def RelativeToAbsolute(coodinate):
    return [coodinate[0] + settings.CanvasRelativePosition[0],
            coodinate[1] + settings.CanvasRelativePosition[1]]


def KeyboardManager(event, Shell):
    if event.type == KEYDOWN:
        for i in range(10):
            if event.key == i + 48:
                Shell.Input(i)

        for i in range(97, 124):
            if event.key == i:
                Shell.Input(chr(i - 32))
        if event.key == K_SPACE:
            Shell.Input(" ")
        if event.key == K_LEFTBRACKET:
            Shell.Input("[")
        if event.key == K_RIGHTBRACKET:
            Shell.Input("]")

        if event.key == 8:
            Shell.Delete()

        if event.key == 13:
            Shell.Exec()


def AngleToRadian(angle):
    return angle / 360 * (2 * math.pi)


def RadianToAngle(radian):
    return radian / (2 * math.pi) * 360


def CutSphere(Arr, start, end):  # return int |  return -1: ERROR
    cul = 1
    Current = start
    while cul != 0:
        Current += 1
        if Current > end:
            return -1
        if Arr[Current] == "[":
            cul += 1
        elif Arr[Current] == "]":
            cul -= 1
    return Current
