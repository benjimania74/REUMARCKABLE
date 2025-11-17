from game.objects.collider.Colliders import Activated, Color, Surface
from .Colliders import *
from ..entity import Player

class PlayerDetectorCollider(ActuatorCollider):
    players: list[Player]
    data: dict[str, Any]

    def __init__(self, x: int, y: int, w: int, h: int, priority: int, hardColliding: bool, activated: Activated, texture: Color | str | None, players: list[Player], surface: Surface) -> None:
        super().__init__(x, y, w, h, priority, hardColliding, activated, texture, surface)
        self.players = players
        self.data = {}
    
    def update(self):
        super().update()
        if self.collidePlayer():
            self.activated.onActuated(self.data)

    def collidePlayer(self) -> bool:
        """Retourne si le joueur touche le detecteur"""
        isTouching: bool = False
        i = 0
        while i < len(self.players) and not isTouching:
            isTouching = self.isColliding(self.players[i])
            i += 1
        return isTouching

class EndGamePlayerDetectorCollider(PlayerDetectorCollider):
    def __init__(self, x: int, y: int, w: int, h: int, priority: int, hardColliding: bool, activated: Activated, texture: Color | str | None, player: Player, surface: Surface) -> None:
        super().__init__(x, y, w, h, priority, hardColliding, activated, texture, [player], surface)
        self.data = {
            "type": self.__class__.__qualname__
        }