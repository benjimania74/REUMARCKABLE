from pygame import Color
from typing import Any

from game.Game import Game
from game.menu import *
from game.levels.Level import Level
from game.Utils import Percent, FRAME_WIDTH, FRAME_HEIGHT
from game.menu import *
from game.objects import *

class Tutorial(Level):
    menu: Menu|None

    def __init__(self, mainMenu: Menu, game: Game) -> None:
        super().__init__(mainMenu, game, "Tutoriel")
        
    def load(self) -> None:
        self.menu = None
        game: Game = self.game
        colliders = self.colliders
        toDisplay = self.content
        actuators = self.actuators

        rectangleCollidersInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int,bool,Color|str|None] ] = [
            (0,200,FRAME_WIDTH//2 - 100,50,51,True,Color(0,255,0)), # sol principal
            (FRAME_WIDTH // 2 - 100, 180, FRAME_WIDTH // 2 + 100, 50, 51, True, Color(0,255,0)), # plateforme basse
            (Percent(50), 280, FRAME_WIDTH // 4, 50, 51, True, Color(50, 230, 65)), # plateforme haut
            (0, 0, 0, FRAME_HEIGHT, 100, True, None), # mur écran gauche
            (FRAME_WIDTH, 0, 0, FRAME_HEIGHT, 100, True, None) # mur écran droit
        ]
        for rci in rectangleCollidersInfo:
            colliders.append( RectangleCollider(*rci, game.getScreen()) )

        p: Player = Player(0,400, 50, 50, "background.jpg", colliders, game.getScreen())
        phantom: PhantomPlayer = PhantomPlayer(0, 350, 50, 50, Color(0,0,255), colliders, game.getScreen())
        colliders.append(p)
        colliders.append(phantom)

        end: EndGamePlayerDetectorCollider = EndGamePlayerDetectorCollider(1000, 320, 50, 10, 51, True, self, Color(0,255,0), p, game.getScreen())
        colliders.append(end)
        self.end = end

        toDisplay += colliders

        actuators.append(
            ActuatorCollider(150,260, 20,10, 0, False, end,"", game.getScreen())
        )

        toDisplay += actuators

        self.player = p
        self.phantom = phantom
        self.activePlayer = p

export: dict[str,Any] = {
    "class_name": Tutorial.__qualname__
}