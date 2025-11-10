from engine.Object import Collideable
from engine.Actuator import Actuator, Activated
from engine.Percent import Percent

from game.Utils import toPygameY, calcPercent
from game.Player import Player
from game.Image import Image

from pygame import Surface, Color, SRCALPHA

class RectangleCollider(Collideable, Activated):
    color: Color|None = None
    image: Image|None = None
    drawSurface: Surface

    def __init__(self, x: int|Percent, y: int|Percent, width: int|Percent, height: int|Percent, priority: int, hardColliding:bool, texture: Color|str|None, drawSurface: Surface) -> None:
        drawSurfaceWidth: int = drawSurface.get_width()
        drawSurfaceHeight: int = drawSurface.get_width()

        self.width = calcPercent(width, drawSurfaceWidth, drawSurfaceWidth)
        self.height = calcPercent(height, drawSurfaceHeight, drawSurfaceHeight)

        self.x = calcPercent(x, drawSurfaceWidth // 2 - self.width // 2, drawSurfaceWidth)
        self.y = calcPercent(y, drawSurfaceHeight // 2 - self.height // 2, drawSurfaceHeight)

        self.priority = priority
        self.hardColliding = hardColliding

        if texture == None or isinstance(texture, Color):
            self.color = texture
        else:
            self.image = Image(
                self.x,
                self.y,
                self.width,
                self.height,
                texture,
                drawSurface
            )
        self.drawSurface = drawSurface
    
    def show(self):
        toDisplay: Surface = Surface((self.width, self.height), SRCALPHA)
        if self.color != None:
            toDisplay.fill(self.color)
            self.drawSurface.blit(
                toDisplay,
                (
                    self.x,
                    toPygameY(self.y, self.height, self.drawSurface.get_height())
                )
            )
        elif self.image != None:
            self.image.show()

class PlayerDetectorCollider(RectangleCollider):
    player: Player
    
    def __init__(self, x: int, y: int, w: int, h: int, priority: int, hardColliding: bool, texture: Color|str, surface: Surface, player: Player) -> None:
        self.player = player
        super().__init__(x, y, w, h, priority, hardColliding, texture, surface)
    
    def collidePlayer(self) -> bool:
        """Retourne si le joueur touche le detecteur"""
        return self.isColliding(self.player)

class ActuatorCollider(RectangleCollider, Actuator):
    def __init__(self, x:int, y:int, w:int, h:int, activated: Activated, texture:Color|str|None, surface:Surface) -> None:
        self.activated = activated
        super().__init__(x, y, w, h, 0, False, texture, surface)