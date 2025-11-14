from .Text import *

from pygame import transform
from pygame.font import Font

from Utils import toPygameY

class DynamicText(Text):
    def __init__(self, x:int|Percent, y:int|Percent, width:int|Percent, height:int|Percent, text:str, fontFile: str|None, fontSize: int, color:Color, backgroundColor:Color|None, drawSurface:Surface) -> None:
        super().__init__(x,y,width,height,text,fontFile,fontSize,color,backgroundColor,drawSurface)
    
    def show(self):
        width: int = self.width
        height: int = self.height
        font: Font = Font(self.fontFile, self.fontSize)
        optimizedTextSize = font.size(self.text)
        if width == 0: width = optimizedTextSize[0]
        if height == 0: height = optimizedTextSize[1]

        toDisplay: Surface = font.render(self.text if self.text != "" else " ", True, self.color)

        if self.backgroundColor != None:
            backgroundSurface: Surface = Surface((width, height), SRCALPHA)
            backgroundSurface.fill( self.backgroundColor )
            backgroundSurface.blit(toDisplay, (0,0))
            toDisplay = backgroundSurface
        
        self.drawSurface.blit(
            transform.scale(toDisplay, (width, height)),
            (
                self.x,
                toPygameY(
                    self.y,
                    height,
                    self.drawSurfaceHeight
                )
            )
        )
    
    def setText(self, text:str):
        self.text = text
    
    def setFontFile(self, fontFile:str|None):
        self.fontFile = fontFile
        
    def setFontSize(self, fontSize:int):
        self.fontSize = fontSize
    
    def setColor(self, color:Color):
        self.color = color
    
    def setBackgroundColor(self, backgroundColor:Color|None):
        self.backgroundColor = backgroundColor