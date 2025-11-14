from pygame import image, Surface, transform

from engine import *

from game.Utils import IMAGE_DIRECTORY, NO_TEXTURE, toPygameY, calcPercent

from os.path import isfile

class Image(Object):
    imageSurface: Surface
    drawSurface: Surface
    drawSurfaceWidth: int
    drawSurfaceHeight: int

    def __init__(self, x:int|Percent, y:int|Percent, width:int|Percent, height:int|Percent, imageName:str, drawSurface: Surface) -> None:
        self.drawSurfaceWidth = drawSurfaceWidth = drawSurface.get_width()
        self.drawSurfaceHeight = drawSurfaceHeight = drawSurface.get_height()

        self.width = calcPercent(width, drawSurfaceWidth, drawSurfaceWidth)
        self.height = calcPercent(height, drawSurfaceHeight, drawSurfaceHeight)

        self.x = calcPercent(x, drawSurfaceWidth // 2 - self.width // 2, drawSurfaceWidth)
        self.y = calcPercent(y, drawSurfaceHeight // 2 - self.height // 2, drawSurfaceHeight)
        
        self.imageSurface = getImage(imageName)
        self.drawSurface = drawSurface

    def show(self):
        self.drawSurface.blit(
            transform.scale(self.imageSurface, (self.width,self.height)),
            (
                self.x,
                toPygameY(self.y, self.height, self.drawSurfaceHeight)
            )
        )
    
    def setCoordinate(self, x:int|Percent,y:int|Percent):
        self.x = calcPercent(x, self.drawSurfaceWidth // 2 - self.width // 2, self.drawSurfaceWidth)
        self.y = calcPercent(y, self.drawSurfaceHeight // 2 - self.height // 2, self.drawSurfaceHeight)
    
    def setSize(self, width:int|Percent, height:int|Percent):
        self.width = calcPercent(width, self.drawSurfaceWidth, self.drawSurfaceWidth)
        self.height = calcPercent(height, self.drawSurfaceHeight, self.drawSurfaceHeight)
    
def getImage(imageName: str) -> Surface:
    """Retourne la surface de l'image demandé"""
    if not isfile(IMAGE_DIRECTORY + imageName):
        imageName = NO_TEXTURE
    return image.load(IMAGE_DIRECTORY + imageName).convert() 
