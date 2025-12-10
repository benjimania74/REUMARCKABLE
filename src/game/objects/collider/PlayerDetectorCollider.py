from game.objects.collider.Colliders import Activated, Color, Surface
from .Colliders import *
from ..entity import Player

class PlayerDetectorCollider(ActuatorCollider):
    players: list[Player]
    data: dict[str, Any]
    actuateOnUpdate: bool

    def __init__(self, x: int|Percent, y: int|Percent, w: int|Percent, h: int|Percent, priority: int, hardColliding: bool, activateds: list[Activated], texture: Color | str | None, players: list[Player], surface: Surface) -> None:
        super().__init__(x, y, w, h, priority, hardColliding, activateds, texture, surface)
        self.players = players
        self.data = {"status":"unactivated"}
        self.actuateOnUpdate = True
    
    def update(self):
        super().update()
        if self.collidePlayer():
            self.onCollide()
        else:
            self.onNotCollide()
    
    def onCollide(self):
        """Actualise le PlayerDetectorCollider lors d'une collision avec l'un des joueurs"""
        actuate: bool = False
        if self.data["status"] == "unactivated":
            actuate = True
        
        self.data["status"] = "activated"

        if actuate:
            self.actuate()

    def onNotCollide(self):
        """Actualise le PlayerDetectorCollider quand il n'y a pas de collision avec l'un des joueurs"""
        actuate: bool = False
        if self.data["status"] == "activated":
            actuate = True
        
        self.data["status"] = "unactivated"

        if actuate:
            self.actuate()

    def collidePlayer(self) -> bool:
        """Retourne si le joueur touche le detecteur"""
        isTouching: bool = False
        i = 0
        while i < len(self.players) and not isTouching:
            isTouching = self.isColliding(self.players[i])
            i += 1
        return isTouching

class EndGamePlayerDetectorCollider(PlayerDetectorCollider):
    def __init__(self, x: int|Percent, y: int|Percent, w: int|Percent, h: int|Percent, priority: int, hardColliding: bool, activated: Activated, texture: Color | str | None, player: Player, surface: Surface) -> None:
        super().__init__(x, y, w, h, priority, hardColliding, [activated], texture, [player], surface)
        self.data["type"] = self.__class__.__qualname__
        #self.data["status"] = "activated"

class ButtonPlayerDetectorCollider(PlayerDetectorCollider):
    actuated: bool

    def __init__(self, x: int|Percent, y: int|Percent, w: int|Percent, h: int|Percent, priority: int, hardColliding: bool, activateds: list[Activated], texture: Color | str | None, players: list[Player], surface: Surface) -> None:
        super().__init__(x, y, w, h, priority, hardColliding, activateds, texture, players, surface)
        self.actuateOnUpdate = False
        self.actuated = False
    
    def actuate(self):
        self.actuated = not self.actuated
        self.data["status"] = "activated" if self.actuated else "unactivated"
        super().actuate()