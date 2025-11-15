from engine import *

from engine import Activated
from game.Utils import toPygameY, calcPercent
from ..image import Image
from ..entity import Player
from ..Rectangle import Rectangle

from pygame import Surface, Color, SRCALPHA

class RectangleCollider(Rectangle, Collideable, Activated):
    color: Color|None = None
    image: Image|None = None
    drawSurface: Surface

    def __init__(self, x: int|Percent, y: int|Percent, width: int|Percent, height: int|Percent, priority: int, hardColliding:bool, texture: Color|str|None, drawSurface: Surface) -> None:
        super().__init__(x,y,width,height,texture,drawSurface)
        self.priority = priority
        self.hardColliding = hardColliding

class ActuatorCollider(RectangleCollider, Actuator):
    def __init__(self, x:int, y:int, w:int, h:int, priority: int, hardColliding: bool, activated: Activated, texture:Color|str|None, surface:Surface) -> None:
        self.activated = activated
        super().__init__(x, y, w, h, priority, hardColliding, texture, surface)

class PlayerDetectorCollider(ActuatorCollider):
    player: Player
    
    def __init__(self, x: int, y: int, w: int, h: int, priority: int, hardColliding: bool, activated: Activated, texture: Color | str | None, player: Player, surface: Surface) -> None:
        super().__init__(x, y, w, h, priority, hardColliding, activated, texture, surface)
        self.player = player
    
    def update(self):
        super().update()
        if self.collidePlayer():
            self.activated.onActuated()

    def collidePlayer(self) -> bool:
        """Retourne si le joueur touche le detecteur"""
        return self.isColliding(self.player)