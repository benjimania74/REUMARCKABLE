from pygame import Surface, Color, SRCALPHA

from engine import *

from .image import *
from game.Utils import calcPercent, toPygameY

class Rectangle(Object):
    toShow: Surface|Image
    drawSurface: Surface

    def __init__(self, x:int|Percent, y:int|Percent, width:int|Percent, height:int|Percent, texture:Color|str|None, drawSurface: Surface) -> None:
        drawSurfaceWidth: int = drawSurface.get_width()
        drawSurfaceHeight: int = drawSurface.get_height()

        self.width = calcPercent(width, drawSurfaceWidth, drawSurfaceWidth)
        self.height = calcPercent(height, drawSurfaceHeight, drawSurfaceHeight)

        self.x = calcPercent(x, drawSurfaceWidth // 2 - self.width // 2, drawSurfaceWidth)
        self.y = calcPercent(y, drawSurfaceHeight // 2 - self.height // 2, drawSurfaceHeight)

        if isinstance(texture, Color) or texture == None:
            toDraw = Surface((self.width, self.height), flags=SRCALPHA)
            toDraw.fill(texture if texture != None else Color(0,0,0,0))
            self.toShow = toDraw
        else:
            self.toShow = Image(self.x,self.y,self.width,self.height,texture,drawSurface)
        
        self.drawSurface = drawSurface
    
    def show(self):
        if isinstance(self.toShow, Surface):
            self.drawSurface.blit(
                self.toShow,
                (
                    self.x,
                    toPygameY(self.y, self.height, self.drawSurface.get_height())
                )
            )
        else:
            self.toShow.show()