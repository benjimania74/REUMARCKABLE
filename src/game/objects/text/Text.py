from engine import *

from game.Utils import calcPercent

from pygame import Surface, Color, SRCALPHA

class Text(Object):
    text: str
    fontFile: str|None
    fontSize: int
    color: Color
    backgroundColor: Color|None
    drawSurface: Surface
    drawSurfaceWidth: int
    drawSurfaceHeight: int

    def __init__(self, x:int|Percent, y:int|Percent, width:int|Percent, height:int|Percent, text:str, fontFile:str|None, fontSize:int, color: Color, backgroundColor: Color|None, drawSurface: Surface) -> None:
        self.drawSurfaceWidth = drawSurfaceWidth = drawSurface.get_width()
        self.drawSurfaceHeight = drawSurfaceHeight = drawSurface.get_height()

        self.width = calcPercent(width, drawSurfaceWidth, drawSurfaceWidth)
        self.height = calcPercent(height, drawSurfaceHeight, drawSurfaceHeight)

        self.x = calcPercent(x, drawSurfaceWidth // 2 - self.width // 2, drawSurfaceWidth)
        self.y = calcPercent(y, drawSurfaceHeight // 2 - self.height // 2, drawSurfaceHeight)

        self.text = text
        self.fontFile = fontFile
        self.fontSize = fontSize
        self.color = color
        self.backgroundColor = backgroundColor
        self.drawSurface = drawSurface

    def setPosition(self, x:int|Percent, y:int|Percent):
        self.x = calcPercent(x, self.drawSurfaceWidth // 2 - self.width // 2, self.drawSurfaceWidth)
        self.y = calcPercent(y, self.drawSurfaceHeight // 2 - self.height // 2, self.drawSurfaceHeight)
    
    def setSize(self, width:int|Percent, height:int|Percent):
        self.width = calcPercent(width, self.drawSurfaceWidth, self.drawSurfaceWidth)
        self.height = calcPercent(height, self.drawSurfaceHeight, self.drawSurfaceHeight)