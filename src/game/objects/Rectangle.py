from pygame import Surface, Color, SRCALPHA

from engine import *

from game.Utils import calcPercent, toPygameY

class Rectangle(Object):
    toDraw: Surface
    drawSurface: Surface

    def __init__(self, x:int|Percent, y:int|Percent, width:int|Percent, height:int|Percent, color:Color, drawSurface: Surface) -> None:
        drawSurfaceWidth: int = drawSurface.get_width()
        drawSurfaceHeight: int = drawSurface.get_height()

        self.width = calcPercent(width, drawSurfaceWidth, drawSurfaceWidth)
        self.height = calcPercent(height, drawSurfaceHeight, drawSurfaceHeight)

        self.x = calcPercent(x, drawSurfaceWidth // 2 - self.width // 2, drawSurfaceWidth)
        self.y = calcPercent(y, drawSurfaceHeight // 2 - self.height // 2, drawSurfaceHeight)

        self.drawSurface = drawSurface

        self.toDraw = Surface((self.width, self.height), flags=SRCALPHA)
        self.toDraw.fill(color)

    def show(self):
        self.drawSurface.blit(
            self.toDraw,
            (
                self.x,
                toPygameY(self.y, self.height, self.drawSurface.get_height())
            )
        )