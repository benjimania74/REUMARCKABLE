from engine.Object import Object
from engine.Percent import Percent

from game.Utils import toPygameY, calcPercent

from pygame import Surface, transform, Color, SRCALPHA
from pygame.font import Font

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