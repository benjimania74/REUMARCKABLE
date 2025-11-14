from __future__ import annotations
from pygame import Surface, Color, SRCALPHA

from typing import Callable

from engine import *

from game.objects.text import StaticText
from game.Utils import toPygameY, calcPercent

class TextButton(Button):
    text: str
    fontFile: str|None
    fontSize: int
    textColor: Color
    backgroundColor: Color|None
    drawSurface: Surface
    clickFunction: Callable[[TextButton], None]|None

    def __init__(self, x:int|Percent, y:int|Percent, width:int|Percent, height:int|Percent, text:str, fontFile:str|None, fontSize:int, textColor: Color|None, backgroundColor: Color|None, clickFunction: Callable[[TextButton],None]|None, drawSurface:Surface) -> None:
        drawSurfaceWidth: int = drawSurface.get_width()
        drawSurfaceHeight: int = drawSurface.get_height()

        width = calcPercent(width, drawSurfaceWidth, drawSurfaceWidth)
        height = calcPercent(height, drawSurfaceHeight, drawSurfaceHeight)
        x = calcPercent(x, drawSurfaceWidth // 2 - width // 2, drawSurfaceWidth)
        y = calcPercent(y, drawSurfaceHeight // 2 - height // 2, drawSurfaceHeight)

        super().__init__(x, y, width, height)
        
        self.text = text
        self.fontFile = fontFile
        self.fontSize = fontSize
        self.textColor = textColor if textColor != None else Color(0,0,0)
        self.backgroundColor = backgroundColor
        self.drawSurface = drawSurface
        self.clickFunction = clickFunction
    
    def setText(self, text:str):
        self.text = text
    
    def getText(self) -> str:
        return self.text

    def setFontFile(self, fontFile:str|None):
        self.fontFile = fontFile

    def getFontFile(self) -> str|None:
        return self.fontFile

    def setFontSize(self, fontSize:int):
        self.fontSize = fontSize
    
    def getFontSize(self) -> int:
        return self.fontSize

    def setTextColor(self, textColor: Color|None):
        self.textColor = textColor if textColor != None else Color(0,0,0)
    
    def getTextColor(self) -> Color:
        return self.textColor

    def setBackgroundColor(self, backgroundColor: Color|None):
        self.backgroundColor = backgroundColor
    
    def getBackgroundColor(self) -> Color|None:
        return self.backgroundColor

    def setOnClick(self, clickFunction: Callable[[TextButton], None]):
        self.clickFunction = clickFunction

    def show(self):
        buttonSurface = Surface((self.width, self.height), SRCALPHA)
        buttonSurface.fill(self.backgroundColor if self.backgroundColor != None else Color(0,0,0,0))

        text: StaticText = StaticText(
            -1,
            -1,
            -1,
            -1,
            self.text,
            self.fontFile,
            self.fontSize,
            self.textColor,
            None,
            buttonSurface
        )
        text.show()

        self.drawSurface.blit(
            buttonSurface,
            (
                self.x,
                toPygameY(
                    self.y,
                    self.height,
                    self.drawSurface.get_height()
                )
            )
        )
    
    def onClick(self):
        if self.clickFunction != None: self.clickFunction(self)