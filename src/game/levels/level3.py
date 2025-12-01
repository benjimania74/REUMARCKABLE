from game.Game import Game
from game.menu import *
from game.levels.Level import Level
from game.Utils import *
from game.menu import *
from game.menu import Menu
from game.objects import *

class DoorLevel(Level):
    def __init__(self, mainMenu: Menu, game: Game) -> None:
        super().__init__(mainMenu, game, "Porte")
    
    def load(self) -> None:
        gameScreen: Surface = self.game.getScreen()

        colliders = self.colliders

        player: Player = Player(0, Percent(50), 50, 50, PLAYER_TEXTURE, self.colliders, gameScreen)
        phantom: PhantomPlayer = PhantomPlayer(0, Percent(40), 50, 50, PHANTOM_TEXTURE, self.colliders, gameScreen)
        colliders += [player, phantom]

        rectangleCollidersInfo: list[ tuple[int|Percent,int|Percent,int|Percent,int|Percent,int,bool,Color|str|None] ] = [
            (0, Percent(30), FRAME_WIDTH, 50, 51, True, GROUND_TEXTURE), # sol principal
            (300, 316, 250, 50, 51, True, GROUND_TEXTURE), # plateforme
            (400, 366, 50, 10, 51, True, GROUND_TEXTURE), # petit mur plateforme
        ]
        for rci in rectangleCollidersInfo:
            colliders.append( RectangleCollider(*rci, gameScreen) )

        door: Door = Door(Percent(80), Percent(30), 50, Percent(30), 50, Percent(5), 51, DOOR_TEXTURE, gameScreen)
        colliders.append(door)

        bpdc: PlayerDetectorCollider = PlayerDetectorCollider(450, 356, 50, 10, 51, False, [door], PLAYER_DETECTOR_COLOR, [player,phantom], gameScreen)
        colliders.append(bpdc)

        end: EndGamePlayerDetectorCollider = EndGamePlayerDetectorCollider(Percent(90), Percent(37), 50, 5, 51, False, self, END_COLLIDER_TEXTURE, player, gameScreen)
        colliders.append(end)

        self.player = player
        self.phantom = phantom
        self.activePlayer = self.player

        self.content += colliders

export: dict[str,Any] = {
    "class_name": DoorLevel.__qualname__
}