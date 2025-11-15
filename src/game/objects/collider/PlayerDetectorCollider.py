from game.objects.collider.Colliders import Activated, Color, Surface
from .Colliders import *
from ..entity import Player

class PlayerDetectorCollider(ActuatorCollider):
    player: Player
    data: dict[str, Any]

    def __init__(self, x: int, y: int, w: int, h: int, priority: int, hardColliding: bool, activated: Activated, texture: Color | str | None, player: Player, surface: Surface) -> None:
        super().__init__(x, y, w, h, priority, hardColliding, activated, texture, surface)
        self.player = player
        self.data = {}
    
    def update(self):
        super().update()
        if self.collidePlayer():
            self.activated.onActuated(self.data)

    def collidePlayer(self) -> bool:
        """Retourne si le joueur touche le detecteur"""
        return self.isColliding(self.player)

class EndGamePlayerDetectorCollider(PlayerDetectorCollider):
    def __init__(self, x: int, y: int, w: int, h: int, priority: int, hardColliding: bool, activated: Activated, texture: Color | str | None, player: Player, surface: Surface) -> None:
        super().__init__(x, y, w, h, priority, hardColliding, activated, texture, player, surface)
        self.data = {
            "type": self.__class__.__qualname__
        }