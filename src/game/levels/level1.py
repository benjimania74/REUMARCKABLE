from pygame import Color
from typing import Any

from game.Game import Game
from game.menu import *
from game.levels.Level import Level
from game.Utils import *
from game.menu import *
from game.objects import *

class Tutorial(Level):
    def __init__(self, mainMenu: Menu, game: Game) -> None:
        super().__init__(mainMenu, game, "Tutoriel")
        
    def load(self) -> None:
        gameScreen: Surface = self.game.getScreen()
        colliders = self.colliders
        toDisplay = self.content
        actuators = self.actuators

        rectangleCollidersInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int,bool,Color|str|None] ] = [
            (0,200,FRAME_WIDTH//2 - 100,50,51,True,GROUND_TEXTURE), # sol principal
            (FRAME_WIDTH // 2 - 100, 180, FRAME_WIDTH // 2 + 100, 50, 51, True, GROUND_TEXTURE), # plateforme basse
            (Percent(50), 280, FRAME_WIDTH // 4, 50, 51, True, GROUND_TEXTURE), # plateforme haut
        ]
        for rci in rectangleCollidersInfo:
            colliders.append( RectangleCollider(*rci, gameScreen) )

        p: Player = Player(0,400, 50, 50, PLAYER_TEXTURE, colliders, gameScreen)
        phantom: PhantomPlayer = PhantomPlayer(0, 350, 50, 50, PHANTOM_TEXTURE, colliders, gameScreen)
        colliders.append(p)
        colliders.append(phantom)

        end: EndGamePlayerDetectorCollider = EndGamePlayerDetectorCollider(1000, 350, 50, 10, 51, True, self, END_COLLIDER_TEXTURE, p, gameScreen)
        colliders.append(end)

        toDisplay += colliders
        toDisplay += actuators

        self.player = p
        self.phantom = phantom
        self.activePlayer = p

export: dict[str,Any] = {
    "class_name": Tutorial.__qualname__
}