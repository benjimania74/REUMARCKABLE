from .Text import *

from pygame import transform
from pygame.font import Font

from Utils import toPygameY

class StaticText(Text):
    toDisplay: Surface
    drawSurface: Surface

    def __init__(self, x:int|Percent, y:int|Percent, width:int|Percent, height:int|Percent, text:str, fontFile: str|None, fontSize: int, color: Color, backgroundColor: Color|None, drawSurface: Surface) -> None:
        super().__init__(x,y,width,height,text,fontFile,fontSize,color,backgroundColor,drawSurface)
        
        font = Font(fontFile, fontSize)
        optimizedTextSize = font.size(text)

        self.width = self.width if self.width != 0 else optimizedTextSize[0]
        self.height = self.height if self.height != 0 else optimizedTextSize[1]

        toDisplay = font.render(text if text != "" else " ", True, color)

        if backgroundColor != None:
            backgroundSurface: Surface = Surface((self.width, self.height), SRCALPHA)
            backgroundSurface.fill(backgroundColor)
            backgroundSurface.blit(toDisplay, (0,0))
            toDisplay = backgroundSurface
        
        self.toDisplay = toDisplay
        self.drawSurface = drawSurface
    
    def show(self):
        self.drawSurface.blit(
            transform.scale(self.toDisplay, (self.width, self.height)),
            (
                self.x,
                toPygameY(self.y, self.height, self.drawSurfaceHeight)
            )
        )