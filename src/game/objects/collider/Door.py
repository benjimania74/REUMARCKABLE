from typing import Any
from pygame import Color, Surface

from engine.Percent import Percent

from .Colliders import RectangleCollider
from game.Utils import calcPercent

class Door(RectangleCollider): # porte avec intérupteurs connectés
    closedWidth: int
    closedHeight: int

    openWidth: int
    openHeight: int

    def __init__(self, x: int | Percent, y: int | Percent, width: int | Percent, height: int | Percent, openWidth: int|Percent, openHeight: int|Percent, priority: int, texture: Color | str | None, drawSurface: Surface) -> None:
        super().__init__(x, y, width, height, priority, True, texture, drawSurface)
        self.closedWidth = self.width
        self.closedHeight = self.height
        self.openWidth = calcPercent(openWidth, 0, self.width)
        self.openHeight = calcPercent(openHeight, 0, self.height)
    
    def onActuated(self, data: dict[str, Any] | None = None) -> None:
        if data == None: return
        
        status: str|None = data.get("status", None)
        
        if status == None: return
        
        if status == "activated":
            self.width = self.openWidth
            self.height = self.openHeight
        else:
            self.width = self.closedWidth
            self.height = self.closedHeight

class ClickDoor(Door): # porte avec levier
    isClosed: bool

    def __init__(self, x: int | Percent, y: int | Percent, width: int | Percent, height: int | Percent, openWidth: int | Percent, openHeight: int | Percent, priority: int, texture: Any | str | None, drawSurface: Surface) -> None:
        super().__init__(x, y, width, height, openWidth, openHeight, priority, texture, drawSurface)
        self.isClosed = True

    def onActuated(self, data: dict[str, Any] | None = None) -> None:
        if self.isClosed:
            self.width = self.openWidth
            self.height = self.openHeight
        else:
            self.width = self.closedWidth
            self.height = self.closedHeight
        self.isClosed = not self.isClosed
